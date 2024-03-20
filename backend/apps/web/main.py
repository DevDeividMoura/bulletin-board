from fastapi import FastAPI
from apps.web.routers import (
    bulletins
)

app = FastAPI()

app.include_router(bulletins.router, prefix="/bulletins", tags=["bulletins"])
