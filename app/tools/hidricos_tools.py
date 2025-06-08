from langchain_core.tools import tool
import httpx
import random
from app.core.config import settings

@tool
def get_soil_moisture(plot_id: str) -> str:
    """
    Obtiene el nivel de humedad del suelo simulado para la parcela 'plot_id'.
    Retorna el porcentaje de humedad y una breve descripción.
    """
    print(f"🛠️ Herramienta 'get_soil_moisture' llamada para parcela: {plot_id}")
    moisture_percentage = random.randint(20, 85) # %
    status = "Óptimo"
    if moisture_percentage < 30: status = "Bajo (Necesita riego)"
    elif moisture_percentage > 75: status = "Alto (Riesgo de anegamiento)"
    return f"Humedad del suelo para parcela {plot_id}: {moisture_percentage}%. Estado: {status}."

@tool
def get_weather_forecast(location: str, days: int = 3) -> str:
    """
    Obtiene el pronóstico del tiempo simulado para una 'location' durante los próximos 'days'.
    Retorna un resumen del pronóstico (temperatura, precipitación).
    """
    print(f"🛠️ Herramienta 'get_weather_forecast' llamada para: {location}, días: {days}")
    # Simulación
    forecasts = []
    for i in range(days):
        temp_min = random.randint(10, 20)
        temp_max = random.randint(temp_min + 5, 35)
        precip_chance = random.randint(0, 100)
        precip_mm = random.uniform(0, 15) if precip_chance > 40 else 0
        forecasts.append(f"Día {i+1}: Temp {temp_min}-{temp_max}°C, Precipitación: {precip_mm:.1f}mm ({precip_chance}% prob.)")
    return f"Pronóstico para {location} ({days} días):\n" + "\n".join(forecasts)

@tool
def get_water_quality(water_source_id: str) -> str:
    """
    Obtiene un informe simulado de calidad del agua para la fuente 'water_source_id'.
    Retorna parámetros clave como pH, EC (Conductividad Eléctrica), y niveles de contaminantes.
    """
    print(f"🛠️ Herramienta 'get_water_quality' llamada para fuente: {water_source_id}")
    ph = random.uniform(6.0, 8.5)
    ec = random.uniform(0.5, 2.5) # dS/m
    contaminants = "Niveles de nitratos dentro de los límites seguros." if random.random() > 0.2 else "Niveles de nitratos ligeramente elevados, monitorear."
    return f"Calidad del agua para {water_source_id}: pH {ph:.1f}, EC {ec:.1f} dS/m. {contaminants}"

@tool
async def get_current_weather(location: str) -> str:
    """
    Obtiene el clima actual para una ubicación específica (ciudad o ciudad,código_país).
    Retorna una descripción textual del clima.
    """
    if not settings.OPENWEATHERMAP_API_KEY:
        return "Servicio de clima no disponible (API key no configurada)."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "es"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            description = data["weather"][0]["description"] if data.get("weather") else "no disponible"
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            return (f"Clima actual en {data.get('name', location)}: {description}, "
                    f"Temperatura: {temp}°C, Humedad: {humidity}%, Viento: {wind_speed} m/s.")
        except httpx.HTTPStatusError as e:
            return f"Error al obtener datos del clima para {location}: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error inesperado al obtener datos del clima para {location}: {str(e)}"

@tool
async def get_daily_forecast(location: str, days: int = 5) -> str:
    """
    Obtiene el pronóstico del tiempo diario para una ubicación (ciudad o ciudad,código_país)
    para los próximos 'days' días (máximo 5-7 dependiendo de la API subyacente).
    Retorna un resumen textual del pronóstico.
    """
    if not settings.OPENWEATHERMAP_API_KEY:
        return "Servicio de clima no disponible (API key no configurada)."

    # Lógica similar al endpoint de FastAPI para llamar a OpenWeatherMap /forecast
    # y formatear la respuesta como un string.
    # (Por brevedad, no repito toda la lógica de procesamiento aquí, pero sería similar)
    # Deberías procesar la respuesta JSON para dar un resumen legible.
    
    # Ejemplo simplificado de lo que la herramienta podría retornar:
    # (Idealmente, llamarías a la misma lógica que el endpoint o a una función compartida)
    base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
    # ... (código para llamar a la API y procesar como en el endpoint) ...
    # Esta es una simulación muy básica del formato de salida:
    
    # Aquí deberías reusar la lógica del endpoint para obtener y procesar los datos.
    # Por simplicidad, voy a simular una llamada a la función del endpoint (esto no funcionaría directamente así)
    # En una implementación real, extraerías la lógica de llamada a OpenWeatherMap a una función helper.
    
    # Simulación de la respuesta de la herramienta:
    # (En una implementación real, esta herramienta llamaría a la API de OpenWeatherMap)
    # y procesaría los datos para devolver un string como el siguiente)
    
    # Lógica de llamada a la API (simplificada para el ejemplo de la herramienta)
    params_forecast = {"q": location, "appid": settings.OPENWEATHERMAP_API_KEY, "units": "metric", "lang": "es"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url_forecast, params=params_forecast)
            response.raise_for_status()
            forecast_data = response.json() # Datos de 5 días / 3 horas

            # Procesamiento para obtener un resumen diario (similar al endpoint)
            # ... (lógica de procesamiento omitida por brevedad, pero necesaria) ...
            
            # Ejemplo de salida formateada:
            output_str = f"Pronóstico para {location} (próximos días):\n"
            # Suponiendo que 'processed_daily_data' es una lista de DailyForecast
            # for day_fc in processed_daily_data_from_api_call[:days]:
            # output_str += f"- {day_fc.date.strftime('%Y-%m-%d')}: {day_fc.description}, Min: {day_fc.temp_min}°C, Max: {day_fc.temp_max}°C\n"
            # return output_str
            return f"Pronóstico simulado para {location}: Lunes - Soleado, 25°C; Martes - Nublado, 22°C..." # Placeholder
        except Exception as e:
            return f"No se pudo obtener el pronóstico para {location}: {str(e)}"

hidricos_tools = [
    get_soil_moisture,
    get_weather_forecast,
    get_water_quality,
    get_current_weather,
    get_daily_forecast,
]