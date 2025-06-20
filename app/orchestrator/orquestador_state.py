from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import BaseMessage

from app.agents.monitoreo_agent import app_monitoreo, agente_monitoreo_descripcion
from app.agents.produccion_agent import app_produccion, agente_produccion_descripcion
from app.agents.hidricos_agent import app_hidrico, agente_hidrico_descripcion
from app.agents.sostenibilidad_agent import app_sostenibilidad, agente_sostenibilidad_descripcion
from app.agents.suministro_cadena_agent import app_cadena_suministro, agente_cadena_descripcion
from app.agents.comercializacion_agent import app_comercializacion, agente_comercializacion_descripcion
from app.agents.gestion_riesgos_agent import app_gestion_riesgos, agente_riesgos_descripcion


class OrchestratorState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_agent: Optional[str] # El nombre del agente que debe actuar a continuación
    original_query: str # Guardamos la consulta original del usuario
    # Podríamos añadir más campos si la orquestación se vuelve más compleja,
    # por ejemplo, para pasar resultados parciales entre agentes.
    # intermediate_results: List[str]
    
agent_names = [
    "Agente de Monitoreo y Diagnóstico de Cultivos",
    "Agente de Optimización de la Producción",
    "Agente de Gestión de Recursos Hídricos",
    "Agente de Sostenibilidad y Prácticas Agrícolas",
    "Agente de Optimización de la Cadena de Suministro",
    "Agente de Intermediación y Comercialización",
    "Agente de Predicción y Mitigación de Riesgos"
]

agent_node_names = {
    "Agente de Monitoreo y Diagnóstico de Cultivos": "monitoreo_cultivos",
    "Agente de Optimización de la Producción": "optimizacion_produccion",
    "Agente de Gestión de Recursos Hídricos": "gestion_hidrica",
    "Agente de Sostenibilidad y Prácticas Agrícolas": "sostenibilidad_agricola",
    "Agente de Optimización de la Cadena de Suministro": "optimizacion_cadena",
    "Agente de Intermediación y Comercialización": "intermediacion_comercializacion",
    "Agente de Predicción y Mitigación de Riesgos": "prediccion_riesgos"
}

agent_apps = {
    "monitoreo_cultivos": app_monitoreo,
    "optimizacion_produccion": app_produccion,
    "gestion_hidrica": app_hidrico,
    "sostenibilidad_agricola": app_sostenibilidad,
    "optimizacion_cadena": app_cadena_suministro,
    "intermediacion_comercializacion": app_comercializacion,
    "prediccion_riesgos": app_gestion_riesgos
}

agent_descriptions_map = {
    "Agente de Monitoreo y Diagnóstico de Cultivos": agente_monitoreo_descripcion,
    "Agente de Optimización de la Producción": agente_produccion_descripcion,
    "Agente de Gestión de Recursos Hídricos": agente_hidrico_descripcion,
    "Agente de Sostenibilidad y Prácticas Agrícolas": agente_sostenibilidad_descripcion,
    "Agente de Optimización de la Cadena de Suministro": agente_cadena_descripcion,
    "Agente de Intermediación y Comercialización": agente_comercializacion_descripcion,
    "Agente de Predicción y Mitigación de Riesgos": agente_riesgos_descripcion
}