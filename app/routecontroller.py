from fastapi import FastAPI
from app.config import Config

from app.routes.profile_intelligence import router as profile_router
from app.routes.semantic_ranker import router as semantic_router
from app.routes.enrich import router as enrich_router
from app.routes.professional_intelligence import router as professional_router
from app.routes.romantic_intelligence import router as romantic_router
from app.routes.describe_professional_intelligence import router as describe_professional_router

def register_routes(app: FastAPI):
    app.include_router(profile_router, prefix=Config.API_PREFIX)
    app.include_router(semantic_router, prefix=Config.API_PREFIX)
    app.include_router(enrich_router, prefix=Config.API_PREFIX)
    app.include_router(professional_router, prefix=Config.API_PREFIX)
    app.include_router(romantic_router, prefix=Config.API_PREFIX)
    app.include_router(describe_professional_router, prefix=Config.API_PREFIX)

    print("All routes registered")
