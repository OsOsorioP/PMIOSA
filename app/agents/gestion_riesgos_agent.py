from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.gestion_riesgos_tools import gestion_riesgos_tools

agente_riesgos_descripcion = """
Eres el Agente de Predicción y Mitigación de Riesgos.
Tu función es identificar y mitigar riesgos relacionados con la producción agrícola y la cadena de suministro.
Utilizas modelos de análisis de riesgos, sistemas de alerta temprana y planes de contingencia (simulados por predict_extreme_weather_event, assess_pest_disease_outbreak_risk, forecast_market_price_volatility, recommend_risk_mitigation_strategy)
para la prevención de pérdidas de cosechas, manejo de riesgos climáticos y respuesta a interrupciones en la cadena de suministro.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_gestion_riesgos_tools = llm.bind_tools(gestion_riesgos_tools)

gestion_riesgos_tool_node = ToolNode(gestion_riesgos_tools)

def agente_gestion_riesgos_node(state: AgentState):
    """
    Nodo del agente de predicción y mitigación de riesgos. Invoca al LLM
    con las herramientas de gestión de riesgos y decide la siguiente acción.
    """
    print("--- AGENTE GESTIÓN RIESGOS NODE ---")
    messages = state['messages']
    response = llm_with_gestion_riesgos_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Gestión Riesgos): {response}")
    return {"messages": [response]}