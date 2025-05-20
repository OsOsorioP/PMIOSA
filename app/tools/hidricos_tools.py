from langchain_core.tools import tool
import random

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

hidricos_tools = [
    get_soil_moisture,
    get_weather_forecast,
    get_water_quality
]