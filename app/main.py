from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.chat import endpoints

app_fastapi = FastAPI(
    title="Plataforma Multiagente de Agricultura Sostenible v2",
    description="API para interactuar con el sistema multiagente iterativo.",
    version="0.2.0"
)

if settings.BACKEND_CORS_ORIGINS:
    app_fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app_fastapi.include_router(endpoints.router, prefix="/api/v1") 

# Endpoint de bienvenida en la raíz de la app (diferente al del router)
@app_fastapi.get("/")
async def app_root():
    return {"message": "Bienvenido a la Plataforma Multiagente de Agricultura Sostenible"}

# Para ejecutar (desde el directorio raíz 'agricultura_multiagente_api/'):
# uvicorn app.main:app_fastapi --reload