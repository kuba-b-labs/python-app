from fastapi import FastAPI
from app.routers.router import router
from app.routers.auth import auth_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Rejestracja routera
app.include_router(router)
app.include_router(auth_router)

@app.get("/health")
def health():
    """Check if API is healthy"""
    return {"status": "ok"}

