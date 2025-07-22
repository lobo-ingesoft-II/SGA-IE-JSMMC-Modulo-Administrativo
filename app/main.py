from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers.portal_admin import router as portal_admin_router
#observabilidad
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from app.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT
import time
from fastapi import Request

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
    
# Middleware de métricas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise e
    finally:
        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method

        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)

        if status >= 400:
            ERROR_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status)).inc()

    return response

# Endpoint para Prometheus
@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
