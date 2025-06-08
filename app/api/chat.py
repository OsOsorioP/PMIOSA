from fastapi import APIRouter, HTTPException
from typing import List, Optional
import uuid 
import httpx
from app.core.config import settings

from pydantic import BaseModel

from app.orchestrator.graph import app_orchestrator_iterative
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage

from app.models.models import ChatRequest, ChatResponse, ChatMessageInput
from app.utils import convert_to_langchain_message, convert_from_langchain_message
from datetime import datetime, date

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print(f"\nRecibida solicitud de chat para query: '{request.original_query}'")
    print(f"Historial de mensajes recibido: {request.messages_history}")

    langchain_messages: List[BaseMessage] = []

    if not request.messages_history:
        print("Nueva conversación. Usando original_query como primer mensaje.")
        langchain_messages.append(HumanMessage(content=request.original_query))
    else:
        for msg_input in request.messages_history:
            langchain_messages.append(convert_to_langchain_message(msg_input))
        print(f"Historial convertido a Langchain: {langchain_messages}")

    if not langchain_messages:
        print("Error: El historial de mensajes de Langchain está vacío después del procesamiento.")
        raise HTTPException(status_code=400, detail="No se proporcionaron mensajes válidos para procesar.")

    orchestrator_input_original_query = request.original_query

    initial_orchestrator_input = {
        "messages": langchain_messages,
        "original_query": orchestrator_input_original_query
    }

    session_id_to_use = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id_to_use}}

    try:
        print(f"Invocando orquestador con input: {initial_orchestrator_input}")
        
        final_orchestrator_state = app_orchestrator_iterative.invoke(
            initial_orchestrator_input
            , config=config # Comentar al no usar checkpointer
        )
        print("--*******************************************************************--\n")
        print(f"Orquestador finalizado. Estado final: {final_orchestrator_state}")
        print("--*******************************************************************--\n")

        response_lc_messages = final_orchestrator_state.get("messages", [])
        
        api_final_state_messages = [convert_from_langchain_message(m) for m in response_lc_messages]
        
        system_reply_this_turn: List[ChatMessageInput] = []
        if api_final_state_messages:
            last_msg_from_system = api_final_state_messages[-1]
            if last_msg_from_system.role == "ai":
                system_reply_this_turn.append(last_msg_from_system)
            else:
                print(f"Advertencia: El último mensaje del estado final no es 'ai'. Mensaje: {last_msg_from_system}")
                system_reply_this_turn.append(ChatMessageInput(role="ai", content="[Procesamiento completado. Revise el historial completo para más detalles.]"))
        else:
            print("Advertencia: El estado final del orquestador no contiene mensajes.")
            system_reply_this_turn.append(ChatMessageInput(role="ai", content="[El sistema no generó una respuesta explícita en este turno.]"))

        return ChatResponse(
            response_messages=system_reply_this_turn,    
            final_state_messages=api_final_state_messages,
            session_id=request.session_id
        )

    except Exception as e:
        print(f"Error durante la ejecución del orquestador en el endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

class WeatherData(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    icon: Optional[str] = None 
    
@router.get("/weather/current", response_model=WeatherData, tags=["Weather"]) 
async def get_current_weather_by_city(city: str, country_code: Optional[str] = None):
    if not settings.OPENWEATHERMAP_API_KEY:
        raise HTTPException(status_code=503, detail="Servicio de clima no disponible (API key no configurada).")

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    query_param = f"{city}"
    if country_code:
        query_param += f",{country_code}"
    
    params = {
        "q": query_param,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Para Celsius
        "lang": "es"        # Para descripciones en español
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
            data = response.json()

            weather_data = WeatherData(
                location=data.get("name", city),
                temperature=data["main"]["temp"],
                description=data["weather"][0]["description"] if data["weather"] else "No disponible",
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                icon=data["weather"][0]["icon"] if data["weather"] else None
            )
            return weather_data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail="API key de clima inválida o no autorizada.")
            elif e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Ciudad '{city}' no encontrada.")
            else:
                print(f"Error al llamar a OpenWeatherMap: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail=f"Error al obtener datos del clima: {e.response.text}")
        except Exception as e:
            print(f"Error inesperado al obtener datos del clima: {e}")
            raise HTTPException(status_code=500, detail="Error interno al procesar la solicitud de clima.")

# Modelo Pydantic para un día del pronóstico
class DailyForecast(BaseModel):
    date: date
    temp_min: float
    temp_max: float
    description: str
    icon: Optional[str] = None

class WeeklyForecastResponse(BaseModel):
    location: str
    forecasts: List[DailyForecast]

@router.get("/weather/forecast/daily", response_model=WeeklyForecastResponse, tags=["Weather"])
async def get_daily_forecast_by_city(city: str, country_code: Optional[str] = None, days: int = 7):
    if not settings.OPENWEATHERMAP_API_KEY:
        raise HTTPException(status_code=503, detail="Servicio de clima no disponible (API key no configurada).")

    # Paso 1: Geocodificar para obtener lat/lon si es necesario (OpenWeatherMap lo hace con q=city)
    # La API de pronóstico de 5 días también acepta q=city
    base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
    query_param = f"{city}"
    if country_code:
        query_param += f",{country_code}"

    params_forecast = {
        "q": query_param,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "es",
        # "cnt": days * 8 # Aproximadamente 8 registros de 3 horas por día
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url_forecast, params=params_forecast)
            response.raise_for_status()
            forecast_data = response.json()

            daily_forecasts_processed = {}
            location_name = forecast_data.get("city", {}).get("name", city)

            for item in forecast_data.get("list", []):
                dt = datetime.fromtimestamp(item["dt"])
                day_date = dt.date()

                if day_date not in daily_forecasts_processed:
                    daily_forecasts_processed[day_date] = {
                        "temps": [],
                        "descriptions": {}, # Contar ocurrencias para la descripción más común
                        "icons": {} # Contar ocurrencias para el ícono más común del día
                    }
                
                daily_forecasts_processed[day_date]["temps"].append(item["main"]["temp"])
                
                desc = item["weather"][0]["description"] if item.get("weather") else "N/A"
                icon = item["weather"][0]["icon"] if item.get("weather") else None

                daily_forecasts_processed[day_date]["descriptions"][desc] = daily_forecasts_processed[day_date]["descriptions"].get(desc, 0) + 1
                if icon:
                    daily_forecasts_processed[day_date]["icons"][icon] = daily_forecasts_processed[day_date]["icons"].get(icon, 0) + 1
            
            final_daily_list: List[DailyForecast] = []
            # Limitar a los 'days' solicitados, aunque la API de 5 días devuelve 5.
            # Ordenar por fecha
            sorted_dates = sorted(daily_forecasts_processed.keys())[:days] 

            for day_date in sorted_dates:
                day_data = daily_forecasts_processed[day_date]
                if not day_data["temps"]: continue

                # Descripción e ícono más comunes del día
                most_common_desc = max(day_data["descriptions"], key=day_data["descriptions"].get) if day_data["descriptions"] else "No disponible"
                most_common_icon = None
                if day_data["icons"]:
                    # Tomar el ícono de la parte diurna (termina en 'd') si está disponible, sino el primero
                    day_icons = [ic for ic in day_data["icons"].keys() if ic.endswith('d')]
                    if day_icons:
                        most_common_icon = max(day_icons, key=lambda i: day_data["icons"][i])
                    else:
                        most_common_icon = max(day_data["icons"], key=day_data["icons"].get)


                final_daily_list.append(
                    DailyForecast(
                        date=day_date,
                        temp_min=min(day_data["temps"]),
                        temp_max=max(day_data["temps"]),
                        description=most_common_desc,
                        icon=most_common_icon
                    )
                )
            
            if not final_daily_list:
                 raise HTTPException(status_code=404, detail=f"No se encontraron datos de pronóstico para '{city}'.")

            return WeeklyForecastResponse(location=location_name, forecasts=final_daily_list)

        except httpx.HTTPStatusError as e:
            # ... (manejo de errores similar al endpoint de clima actual) ...
            raise HTTPException(status_code=e.response.status_code, detail=f"Error al obtener pronóstico: {e.response.text}")
        except Exception as e:
            print(f"Error inesperado al obtener pronóstico: {e}")
            raise HTTPException(status_code=500, detail="Error interno al procesar la solicitud de pronóstico.")

@router.get("/", include_in_schema=False)
async def api_v1_root():
    return {"message": "API v1 de Agricultura Multiagente"}