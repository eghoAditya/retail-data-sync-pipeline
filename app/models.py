from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from .database import Base


class SalesEvent(Base):
    __tablename__ = "sales_events"

    id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(String(50), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="INR")
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING / PROCESSED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False)
