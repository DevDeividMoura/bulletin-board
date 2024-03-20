from fastapi import FastAPI

from apps.web.main import app as webui_app

from config import (
    WEBUI_NAME,
    ENV,
    VERSION,
    FRONTEND_BUILD_DIR
)
from constants import ERROR_MESSAGES

app = FastAPI(docs_url="/docs" if ENV == "dev" else None, redoc_url=None)

app.mount("/api/v1", webui_app)

@app.get("/api/version")
async def get_app_config():

    return {
        "version": VERSION,
    }

