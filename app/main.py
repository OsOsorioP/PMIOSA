from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.chat import router

app_fastapi = FastAPI(
    title="Plataforma Multiagente de Agricultura Sostenible v2",
    description="API para interactuar con el sistema multiagente iterativo.",
    version="0.2.0"
)

settings

origins = ["http://localhost:5173",]

app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)

app_fastapi.include_router(router, prefix="/api/v1") 

@app_fastapi.get("/")
async def app_root():
    return {"message": "Bienvenido a la Plataforma Multiagente de Agricultura Sostenible"}
