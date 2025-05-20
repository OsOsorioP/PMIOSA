import random
from langchain_core.tools import tool

@tool
def predict_extreme_weather_event(location: str, time_horizon_days: int) -> str:
    """
    Predice la probabilidad simulada de eventos climáticos extremos (heladas, sequías, inundaciones)
    en 'location' dentro de un 'time_horizon_days'.
    Retorna un informe de riesgo.
    """
    print(f"🛠️ Herramienta 'predict_extreme_weather_event' llamada para: {location}, horizonte: {time_horizon_days} días")
    # Simulación

    events = ["heladas tardías", "ola de calor", "sequía prolongada", "fuertes lluvias e inundaciones"]
    risk_level = ["bajo", "moderado", "alto"]
    chosen_event = random.choice(events)
    chosen_risk = random.choice(risk_level)
    probability = random.randint(10, 70) if chosen_risk != "bajo" else random.randint(0,20)

    return f"Predicción de riesgo climático para {location} en los próximos {time_horizon_days} días: Evento: {chosen_event}, Nivel de Riesgo: {chosen_risk} (Probabilidad estimada: {probability}%)."

@tool
def assess_pest_disease_outbreak_risk(plot_id: str, crop_type: str, historical_data_id: str, current_conditions_summary: str) -> str:
    """
    Evalúa el riesgo simulado de brotes de plagas o enfermedades para 'crop_type' en 'plot_id',
    usando 'historical_data_id' y 'current_conditions_summary' (clima, estado del cultivo).
    Retorna una evaluación del riesgo y posibles plagas/enfermedades.
    """
    print(f"🛠️ Herramienta 'assess_pest_disease_outbreak_risk' llamada para parcela: {plot_id}, cultivo: {crop_type}")
    # Simulación

    pests_diseases = {
        "maiz": ["gusano cogollero", "roya común"],
        "trigo": ["pulgón de la espiga", "septoriosis"],
        "tomate": ["mosca blanca", "mildiu"],
        "soja": ["chinche apestosa", "roya asiática"]
    }
    risk_level = ["bajo", "moderado", "alto"]
    target_pd = random.choice(pests_diseases.get(crop_type.lower(), ["plaga genérica", "enfermedad genérica"]))
    chosen_risk = random.choice(risk_level)
    return f"Evaluación de riesgo de plagas/enfermedades para {crop_type} en parcela {plot_id}: Riesgo {chosen_risk} de brote de {target_pd} basado en datos históricos ({historical_data_id}) y condiciones actuales ({current_conditions_summary[:50]}...). Se recomienda monitoreo."

@tool
def forecast_market_price_volatility(product: str, time_horizon_months: int) -> str:
    """
    Pronostica la volatilidad simulada de precios de mercado para un 'product'
    en un 'time_horizon_months'.
    Retorna un índice de volatilidad y factores influyentes.
    """
    print(f"🛠️ Herramienta 'forecast_market_price_volatility' llamada para: {product}, horizonte: {time_horizon_months} meses")
    # Simulación

    volatility_levels = ["baja", "media", "alta"]
    chosen_volatility = random.choice(volatility_levels)
    factors = ["condiciones climáticas globales", "políticas comerciales", "demanda de biocombustibles", "oferta de principales productores"]
    influencing_factors = random.sample(factors, random.randint(1,3))
    return f"Pronóstico de volatilidad de precios para {product} en los próximos {time_horizon_months} meses: Volatilidad {chosen_volatility}. Factores clave: {', '.join(influencing_factors)}."

@tool
def recommend_risk_mitigation_strategy(risk_type: str, risk_details: str, context_info: str) -> str:
    """
    Recomienda estrategias simuladas de mitigación para un 'risk_type' (ej. climático, plaga, mercado)
    con 'risk_details' específicos y 'context_info' (cultivo, región, etc.).
    Retorna una o más estrategias sugeridas.
    """
    print(f"🛠️ Herramienta 'recommend_risk_mitigation_strategy' llamada para riesgo: {risk_type}")
    # Simulación
    strategies = {
        "climático": ["Diversificar fechas de siembra.", "Implementar sistemas de riego eficientes.", "Considerar seguros agrícolas.", "Usar variedades resistentes a sequía/calor."],
        "plaga": ["Rotación de cultivos.", "Control biológico.", "Monitoreo constante y umbrales de acción.", "Uso de variedades resistentes."],
        "mercado": ["Diversificar canales de venta.", "Contratos a futuro (si disponibles).", "Almacenamiento para venta en mejores condiciones.", "Agregar valor al producto (procesamiento)."]
    }
    default_strategies = ["Monitoreo continuo.", "Plan de contingencia actualizado."]
    recs = strategies.get(risk_type.lower(), default_strategies)

    num_recs = random.randint(1, len(recs))
    return f"Estrategias de mitigación recomendadas para riesgo '{risk_type}' ({risk_details}): {'; '.join(random.sample(recs, num_recs))}"

gestion_riesgos_tools = [
    predict_extreme_weather_event,
    assess_pest_disease_outbreak_risk,
    forecast_market_price_volatility,
    recommend_risk_mitigation_strategy
]