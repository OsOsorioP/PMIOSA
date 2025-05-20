import random
import uuid
from langchain_core.tools import tool

@tool
def find_potential_buyers(product_type: str, quantity_available_kg: float, quality_grade: str, location: str) -> str:
    """
    Busca compradores potenciales simulados para un 'product_type' con 'quantity_available_kg',
    'quality_grade' (ej. Premium, Grado A) y 'location' del producto.
    Retorna una lista de compradores interesados con sus posibles ofertas.
    """
    print(f"🛠️ Herramienta 'find_potential_buyers' llamada para: {product_type}, cantidad: {quantity_available_kg} kg, calidad: {quality_grade}, ubicación: {location}")
    # Simulación
    buyers = []

    num_buyers = random.randint(1, 3)
    for i in range(num_buyers):
        buyer_name = f"Comprador_{chr(65+i)}_{random.randint(100,999)}"
        offer_price_factor = {"Premium": 1.1, "Grado A": 1.0, "Grado B": 0.9}.get(quality_grade, 0.95)
        base_price = {"maiz": 0.2, "trigo": 0.25, "soja": 0.4, "tomate": 1.5, "lechuga": 1.0}.get(product_type.lower(), 0.1) # Precio base por kg
        offered_price = base_price * offer_price_factor * random.uniform(0.95, 1.05)
        buyers.append(f"{buyer_name} interesado en {random.randint(int(quantity_available_kg/2), int(quantity_available_kg))} kg, ofrece aprox. {offered_price:.2f} USD/kg.")
    if not buyers: return f"No se encontraron compradores inmediatos para {product_type} de calidad {quality_grade} en {location}."
    return f"Compradores potenciales para {product_type}:\n" + "\n".join(buyers)

@tool
def verify_compliance_requirements(product_type: str, destination_market: str) -> str:
    """
    Verifica los requisitos de cumplimiento simulados (certificaciones, normativas)
    para vender 'product_type' en un 'destination_market' (ej. UE, USA, Local).
    Retorna una lista de requisitos clave.
    """
    print(f"🛠️ Herramienta 'verify_compliance_requirements' llamada para: {product_type}, mercado: {destination_market}")
    # Simulación
    requirements = {
        "UE": ["Certificación GlobalG.A.P.", "Límites Máximos de Residuos (LMR) de la UE", "Etiquetado según normativa UE."],
        "USA": ["Cumplimiento FDA (FSMA)", "Certificación USDA Organic (si aplica)", "Requisitos de importación específicos."],
        "Local": ["Registro sanitario local", "Buenas prácticas de manufactura (BPM)."]
    }
    market_reqs = requirements.get(destination_market, ["Consultar normativa específica del mercado de destino."])
    return f"Requisitos de cumplimiento para {product_type} en mercado {destination_market}: {'; '.join(market_reqs)}"

@tool
def draft_sales_agreement(seller_info: str, buyer_info: str, product_details: str, terms: str) -> str:
    """
    Genera un borrador simulado de acuerdo de venta basado en 'seller_info', 'buyer_info',
    'product_details' (tipo, cantidad, calidad, precio) y 'terms' (condiciones de pago, entrega).
    Retorna un ID o texto del borrador del acuerdo.
    """
    print(f"🛠️ Herramienta 'draft_sales_agreement' llamada.")
    # Simulación
    agreement_id = f"AGR_{uuid.uuid4()}"
    return f"Borrador de acuerdo de venta {agreement_id} generado. Detalles:\nVendedor: {seller_info}\nComprador: {buyer_info}\nProducto: {product_details}\nTérminos: {terms}\n---\nEste es un borrador y debe ser revisado legalmente."

@tool
def create_product_listing(product_name: str, description: str, price: float, quantity_kg: float, images_urls: list, platform: str = "plataforma_interna") -> str:
    """
    Crea un listado de producto simulado en una 'platform' (ej. plataforma_interna, e_commerce_externo)
    con 'product_name', 'description', 'price' por kg, 'quantity_kg' disponible, y 'images_urls'.
    Retorna el ID o URL del listado creado.
    """
    print(f"🛠️ Herramienta 'create_product_listing' llamada para: {product_name} en {platform}")
    # Simulación
    listing_id = f"LIST_{platform.replace('_','')}_{uuid.uuid4()}"
    return f"Listado de producto '{product_name}' creado en {platform} con ID: {listing_id}. Precio: {price}/kg, Cantidad: {quantity_kg}kg. Imágenes: {', '.join(images_urls)}"

comercializacion_tools = [
    find_potential_buyers,
    verify_compliance_requirements,
    draft_sales_agreement,
    create_product_listing
]