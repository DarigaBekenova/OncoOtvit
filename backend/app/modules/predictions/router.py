from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_session

from . import service
from .schemas import DemoSample, ModelMetrics, PredictionCreate, PredictionOut

router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])


@router.get("/samples", response_model=list[DemoSample])
def list_samples() -> list[DemoSample]:
    return service.get_demo_samples()


@router.get("/metrics", response_model=ModelMetrics)
def model_metrics() -> ModelMetrics:
    return service.get_model_metrics()


@router.post("", response_model=PredictionOut, status_code=201)
def create_prediction(
    data: PredictionCreate,
    sample_name: str = Query(default="Пользовательский образец", max_length=100),
    reference_class: str = Query(default="неизвестно", max_length=20),
    session: Session = Depends(get_session),
) -> PredictionOut:
    return service.create_prediction(session, data, sample_name, reference_class)


@router.get("", response_model=list[PredictionOut])
def list_predictions(
    limit: int = Query(default=20, ge=1, le=100), session: Session = Depends(get_session)
) -> list[PredictionOut]:
    return service.list_predictions(session, limit)
