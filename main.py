from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config
from app.routecontroller import register_routes

app = FastAPI(title=Config.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOW_ORIGINS,
    allow_credentials=Config.ALLOW_CREDENTIALS,
    allow_methods=Config.ALLOW_METHODS,
    allow_headers=Config.ALLOW_HEADERS,
)

register_routes(app)
