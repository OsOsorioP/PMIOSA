import uuid
from langchain_core.tools import tool

@tool
def get_vegetation_index_map(latitude: float, longitude: float, date: str) -> str:
    """
    Obtiene un mapa simulado del índice de vegetación (ej. NDVI) para una ubicación geográfica
    (latitud, longitud) y una fecha específica.
    Retorna una URL o identificador del mapa generado.
    """
    print(f"🛠️ Herramienta 'get_vegetation_index_map' llamada con lat: {latitude}, lon: {longitude}, fecha: {date}")
    # Simulación: Podría ser una URL a una imagen o un ID de un sistema GIS
    return f"map_id_ndvi_{uuid.uuid4()}_for_{latitude}_{longitude}_on_{date}.png"

@tool
def check_water_stress_indicators(plot_id: str, date: str) -> str:
    """
    Revisa los indicadores simulados de estrés hídrico para una parcela de cultivo específica
    identificada por 'plot_id' en una fecha determinada.
    Retorna un resumen del estado de estrés hídrico.
    """
    print(f"🛠️ Herramienta 'check_water_stress_indicators' llamada para parcela: {plot_id}, fecha: {date}")
    # Simulación
    stress_levels = ["bajo", "moderado", "alto"]
    import random
    level = random.choice(stress_levels)
    return f"Informe de estrés hídrico para parcela {plot_id} en {date}: Nivel de estrés {level}. Humedad del suelo: {random.randint(30, 70)}%."

@tool
def identify_potential_issues(image_analysis_report_id: str) -> str:
    """
    Analiza un informe simulado de análisis de imágenes (identificado por 'image_analysis_report_id')
    para identificar posibles problemas en los cultivos como plagas, enfermedades o deficiencias nutricionales.
    Retorna una lista de problemas potenciales detectados.
    """
    print(f"🛠️ Herramienta 'identify_potential_issues' llamada con reporte ID: {image_analysis_report_id}")
    # Simulación
    possible_issues = [
        "Posible deficiencia de nitrógeno en sector N-E.",
        "Indicios de actividad de pulgones en hojas inferiores.",
        "Manchas foliares compatibles con mildiu detectadas en área central."
    ]
    import random
    num_issues = random.randint(0, len(possible_issues))
    detected = random.sample(possible_issues, num_issues)
    if not detected:
        return "No se detectaron problemas significativos en el análisis de imágenes."
    return f"Problemas potenciales identificados a partir de {image_analysis_report_id}: {'; '.join(detected)}"

@tool
def request_field_scouting(plot_id: str, issue_description: str, urgency: str = "media") -> str:
    """
    Genera una solicitud simulada para una inspección de campo (scouting) en la parcela 'plot_id'
    debido a un 'issue_description' específico. Se puede especificar la 'urgency' (alta, media, baja).
    Retorna un ID de confirmación de la solicitud.
    """
    print(f"🛠️ Herramienta 'request_field_scouting' llamada para parcela: {plot_id}, problema: {issue_description}, urgencia: {urgency}")
    # Simulación
    request_id = f"scout_req_{uuid.uuid4()}"
    return f"Solicitud de inspección de campo {request_id} creada para la parcela {plot_id} con urgencia {urgency} debido a: {issue_description}. Un técnico será asignado."

monitoreo_tools = [
    get_vegetation_index_map,
    check_water_stress_indicators,
    identify_potential_issues,
    request_field_scouting
]