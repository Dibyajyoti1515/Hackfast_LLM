from fastapi import FastAPI
from app.config import Config

from app.routes.profile_intelligence import router as profile_router

def register_routes(app: FastAPI):
    app.include_router(profile_router, prefix=Config.API_PREFIX)

    print("All routes registered")
