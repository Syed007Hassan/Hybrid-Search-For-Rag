"""
    The entry file for the FastAPI application.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("This is an info message.")

app = FastAPI(title="Hybrid Search with Postgres", version="1.0", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
