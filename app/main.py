from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers.portal_admin import router as portal_admin_router

app = FastAPI()

# Incluir el router de la nueva API Portal Administrativo
app.include_router(portal_admin_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gestión Administrativa"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
