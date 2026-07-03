from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Banking Multi-Agent API",
    version="1.0",
)

app.include_router(router)