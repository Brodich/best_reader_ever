import os.path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Settings(BaseSettings):
    project_title: str = Field(alias="PROJECT_TITLE")
    fastapi_host: str = Field(alias="FASTAPI_HOST")
    fastapi_port: int = Field(alias="FASTAPI_PORT")

    model_config = SettingsConfigDict(env_file=os.path.join(base_path, ".env"))


# print(base_path)
settings = Settings()
