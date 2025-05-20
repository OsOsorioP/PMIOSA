import random
from langchain_core.tools import tool

@tool
def get_crop_health_index(plot_id: str, date: str) -> str:
    """
    Obtiene un índice de salud simulado para los cultivos en la parcela 'plot_id' en la fecha 'date'.
    El índice varía de 0 (muy malo) a 100 (excelente).
    """
    print(f"🛠️ Herramienta 'get_crop_health_index' llamada para parcela: {plot_id}, fecha: {date}")
    import random
    health_index = random.randint(60, 95)
    return f"Índice de salud del cultivo para la parcela {plot_id} en {date}: {health_index}/100."

@tool
def predict_yield(plot_id: str, crop_type: str, current_growth_stage: str) -> str:
    """
    Predice el rendimiento simulado para un 'crop_type' específico en la 'plot_id',
    considerando su 'current_growth_stage'.
    Retorna una estimación del rendimiento (ej. toneladas por hectárea).
    """
    print(f"🛠️ Herramienta 'predict_yield' llamada para parcela: {plot_id}, cultivo: {crop_type}, etapa: {current_growth_stage}")
    import random
    base_yield = {"maiz": 8, "trigo": 5, "soja": 3} # Toneladas/ha base
    factor_crecimiento = {"inicial": 0.7, "vegetativo": 0.9, "floracion": 1.1, "maduracion": 1.0}
    rendimiento_estimado = base_yield.get(crop_type.lower(), 4) * factor_crecimiento.get(current_growth_stage.lower(), 1.0) * random.uniform(0.8, 1.2)
    return f"Predicción de rendimiento para {crop_type} en parcela {plot_id} (etapa {current_growth_stage}): {rendimiento_estimado:.2f} ton/ha."

@tool
def recommend_fertilizer_application(plot_id: str, soil_analysis_id: str, crop_type: str) -> str:
    """
    Recomienda una aplicación de fertilizante simulada para la 'plot_id' y 'crop_type',
    basándose en un 'soil_analysis_id' (ID de un análisis de suelo).
    Retorna el tipo y cantidad de fertilizante recomendado.
    """
    print(f"🛠️ Herramienta 'recommend_fertilizer_application' llamada para parcela: {plot_id}, análisis: {soil_analysis_id}, cultivo: {crop_type}")
    # Simulación
    fertilizers = ["NPK 15-15-15", "Urea", "Sulfato de Amonio"]
    import random
    chosen_fertilizer = random.choice(fertilizers)
    amount = random.randint(100, 300) # kg/ha
    return f"Recomendación para {crop_type} en parcela {plot_id} (basado en {soil_analysis_id}): Aplicar {amount} kg/ha de {chosen_fertilizer}."

@tool
def predict_optimal_harvest_window(plot_id: str, crop_type: str, current_maturity_indicators: str) -> str:
    """
    Predice la ventana óptima de cosecha simulada para 'crop_type' en 'plot_id',
    basándose en 'current_maturity_indicators' (ej. contenido de humedad del grano, color).
    Retorna un rango de fechas.
    """
    print(f"🛠️ Herramienta 'predict_optimal_harvest_window' llamada para parcela: {plot_id}, cultivo: {crop_type}, indicadores: {current_maturity_indicators}")
    # Simulación
    import datetime
    from datetime import timedelta
    start_days = random.randint(5, 15)
    end_days = start_days + random.randint(3, 7)
    today = datetime.date.today()
    start_date = today + timedelta(days=start_days)
    end_date = today + timedelta(days=end_days)
    return f"Ventana óptima de cosecha estimada para {crop_type} en parcela {plot_id}: Del {start_date.strftime('%Y-%m-%d')} al {end_date.strftime('%Y-%m-%d')}."

produccion_tools = [
    get_crop_health_index,
    predict_yield,
    recommend_fertilizer_application,
    predict_optimal_harvest_window
]