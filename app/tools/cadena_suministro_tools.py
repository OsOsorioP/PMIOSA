import random
from langchain_core.tools import tool

@tool
def get_market_price_data(product: str, region: str, date: str) -> str:
    """
    Obtiene datos simulados de precios de mercado para un 'product' agrícola en una 'region'
    específica para una 'date' dada.
    Retorna el precio promedio y rango.
    """
    print(f"🛠️ Herramienta 'get_market_price_data' llamada para producto: {product}, región: {region}, fecha: {date}")

    base_prices = {"maiz": 200, "trigo": 250, "soja": 400, "tomate": 1.5, "lechuga": 1} # USD/ton o USD/kg
    price = base_prices.get(product.lower(), 100) * random.uniform(0.9, 1.1)
    price_range = f"{price*0.95:.2f} - {price*1.05:.2f}"
    unit = "USD/ton" if product.lower() in ["maiz", "trigo", "soja"] else "USD/kg"
    return f"Precio de mercado para {product} en {region} ({date}): Promedio {price:.2f} {unit}, Rango {price_range} {unit}."

@tool
def get_transport_options(origin: str, destination: str, product_volume_kg: float) -> str:
    """
    Obtiene opciones de transporte simuladas desde un 'origin' a un 'destination'
    para un 'product_volume_kg' específico.
    Retorna opciones con costo estimado y tiempo de tránsito.
    """
    print(f"🛠️ Herramienta 'get_transport_options' llamada de {origin} a {destination}, volumen: {product_volume_kg} kg")
    # Simulación
    options = []
    if product_volume_kg < 1000:
        options.append(f"Transporte local (furgoneta): Costo estimado {product_volume_kg*0.1:.2f} USD, Tiempo 1-2 días.")
    options.append(f"Camión estándar: Costo estimado {product_volume_kg*0.05:.2f} USD, Tiempo 2-4 días.")
    if product_volume_kg > 10000:
        options.append(f"Tren (si aplica): Costo estimado {product_volume_kg*0.03:.2f} USD, Tiempo 5-7 días.")
    if not options: return "No se encontraron opciones de transporte para los parámetros dados."
    return f"Opciones de transporte de {origin} a {destination} para {product_volume_kg} kg:\n" + "\n".join(options)

@tool
def get_storage_availability(location: str, product_type: str, required_capacity_ton: float) -> str:
    """
    Verifica la disponibilidad simulada de almacenamiento en 'location' para 'product_type'
    y 'required_capacity_ton'.
    Retorna información sobre disponibilidad y costos.
    """
    print(f"🛠️ Herramienta 'get_storage_availability' llamada en: {location}, producto: {product_type}, capacidad: {required_capacity_ton} ton")

    if random.random() > 0.3: # 70% chance de disponibilidad
        cost_per_ton_month = random.uniform(5, 20)
        return f"Almacenamiento disponible en {location} para {product_type}. Capacidad suficiente para {required_capacity_ton} ton. Costo estimado: {cost_per_ton_month:.2f} USD/ton/mes."
    else:
        return f"No hay disponibilidad inmediata de almacenamiento para {required_capacity_ton} ton de {product_type} en {location}. Se recomienda buscar alternativas o reservar con antelación."

@tool
def simulate_sales_scenario(product: str, quantity_kg: float, price_per_kg: float, channel: str) -> str:
    """
    Simula un escenario de ventas para un 'product' con una 'quantity_kg' y 'price_per_kg'
    a través de un 'channel' (ej. mercado local, exportación, supermercado).
    Retorna ingresos estimados y posibles comisiones/costos.
    """
    print(f"🛠️ Herramienta 'simulate_sales_scenario' llamada para: {product}, cantidad: {quantity_kg} kg, precio: {price_per_kg}/kg, canal: {channel}")
    total_revenue = quantity_kg * price_per_kg
    commission_rate = {"mercado local": 0.05, "exportación": 0.15, "supermercado": 0.20}
    commission = total_revenue * commission_rate.get(channel.lower(), 0.10)
    net_revenue = total_revenue - commission
    return f"Simulación de ventas para {quantity_kg} kg de {product} a {price_per_kg}/kg vía {channel}:\nIngresos Brutos: {total_revenue:.2f} USD\nComisión/Costos Estimados ({channel}): {commission:.2f} USD\nIngresos Netos Estimados: {net_revenue:.2f} USD."

cadena_suministro_tools = [
    get_market_price_data,
    get_transport_options,
    get_storage_availability,
    simulate_sales_scenario
]