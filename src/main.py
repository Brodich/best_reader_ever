from fastapi import FastAPI

app = FastAPI(
    # title=settings.FASTAPI_TITLE,
    # version=settings.FASTAPI_VERSION,
    # description=settings.FASTAPI_DESCRIPTION,
    # docs_url=settings.FASTAPI_DOCS_URL,
    # redoc_url=settings.FASTAPI_REDOCS_URL,
    # openapi_url=settings.FASTAPI_OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include()
