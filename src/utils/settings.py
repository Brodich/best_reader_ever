from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str

    # fatapi
    FASTAPI_API_V1_PATH: str = "/api/v1"
    FASTAPI_TITLE: str = "FastAPI"
    FASTAPI_VERSION: str = "0.0.1"
    FASTAPI_DESCRIPTION: str = "Redaify"
    FASTAPI_DOCS_URL: str = f"/api/v1/docs"
    FASTAPI_OPENAPI_URL: str | None = f"/api/v1/docs/openapi"

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    PAGE_LINES: int
    PAGE_CHARS: int

    class Config:
        env_file = f".env"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
