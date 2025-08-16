import uvicorn

from utils.settings import settings


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", 
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=True
    )
