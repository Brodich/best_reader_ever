from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.route import route
from src.utils.settings import settings

app = FastAPI(
    title=settings.FASTAPI_TITLE,
    version=settings.FASTAPI_VERSION,
    description=settings.FASTAPI_DESCRIPTION,
    docs_url=settings.FASTAPI_DOCS_URL,
    openapi_url=settings.FASTAPI_OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(route)
