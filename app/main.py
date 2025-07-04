from fastapi import FastAPI
from app.routers.router import router

app = FastAPI()

app.include_router(router)


@app.get("/health")
def health():
    """Check if API is healthy"""
    #TO DO - add database connection check
    return { "status" : "ok" }


