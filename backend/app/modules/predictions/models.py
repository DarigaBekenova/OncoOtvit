from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_name: Mapped[str] = mapped_column(String(100))
    reference_class: Mapped[str] = mapped_column(String(20))
    predicted_class: Mapped[str] = mapped_column(String(20))
    malignant_probability: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
