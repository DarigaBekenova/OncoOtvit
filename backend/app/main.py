from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.predictions.router import router as predictions_router

app = FastAPI(
    title="ОнкоОтвет — исследовательский API",
    description="Демонстрационный прогноз на синтетических данных. Не использовать для медицинских решений.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(predictions_router)
