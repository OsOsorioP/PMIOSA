import random
from langchain_core.tools import tool

@tool
def search_sustainable_practices(crop_type: str, region_characteristics: str) -> str:
    """
    Busca prácticas agrícolas sostenibles simuladas adecuadas para un 'crop_type'
    y 'region_characteristics' (ej. tipo de suelo, clima).
    Retorna una lista de prácticas recomendadas.
    """
    print(f"🛠️ Herramienta 'search_sustainable_practices' llamada para cultivo: {crop_type}, región: {region_characteristics}")
    # Simulación
    practices = [
        "Rotación de cultivos con leguminosas.",
        "Siembra directa para conservación de suelo y agua.",
        "Uso de cubiertas vegetales en invierno.",
        "Manejo integrado de plagas (MIP).",
        "Compostaje de residuos orgánicos."
    ]

    num_practices = random.randint(2, len(practices))
    return f"Prácticas sostenibles recomendadas para {crop_type} en {region_characteristics}: {'; '.join(random.sample(practices, num_practices))}"

@tool
def assess_practice_impact(practice_name: str, context: str) -> str:
    """
    Evalúa el impacto simulado (ambiental, económico) de una 'practice_name' agrícola sostenible
    en un 'context' específico (ej. reducción de emisiones, mejora de la biodiversidad).
    Retorna una breve evaluación del impacto.
    """
    print(f"🛠️ Herramienta 'assess_practice_impact' llamada para práctica: {practice_name}, contexto: {context}")
    # Simulación
    impacts = {
        "Rotación de cultivos con leguminosas": "Positivo: Mejora la fertilidad del suelo, reduce necesidad de fertilizantes nitrogenados.",
        "Siembra directa": "Positivo: Reduce erosión, mejora retención de agua, secuestra carbono.",
        "Manejo integrado de plagas (MIP)": "Positivo: Reduce uso de pesticidas, protege polinizadores, menor costo a largo plazo."
    }
    default_impact = "Impacto positivo en la sostenibilidad general, contribuye a la salud del ecosistema agrícola."
    return impacts.get(practice_name, default_impact)

sostenibilidad_tools = [
    search_sustainable_practices,
    assess_practice_impact,
]