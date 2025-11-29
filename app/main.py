from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
import logging

# ---------- Logging ----------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Database Setup ----------

# Matches your Docker container:
# docker run --name retail-mysql \
#   -e MYSQL_ROOT_PASSWORD=password \
#   -e MYSQL_DATABASE=retaildb \
#   -p 3306:3306 \
#   -d mysql:8
DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/retaildb"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------- SQLAlchemy Model ----------

class SaleEvent(Base):
    __tablename__ = "sale_events"

    id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(String(50), index=True, nullable=False)
    receipt_id = Column(String(100), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="INR")
    status = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# Create tables if not exist
Base.metadata.create_all(bind=engine)


# ---------- FastAPI App ----------

app = FastAPI(title="Retail Data Sync Pipeline")


# ---------- Dependency ----------

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic Schemas ----------

class SaleEventIn(BaseModel):
    terminal_id: str
    receipt_id: str
    amount: float
    currency: Optional[str] = "INR"


class SaleEventOut(BaseModel):
    id: int
    terminal_id: str
    receipt_id: str
    amount: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows returning ORM objects directly


# ---------- Routes ----------

@app.get("/health")
def health_check():
    """
    Simple health check for the service.
    """
    return {"status": "ok"}


@app.post("/events", response_model=SaleEventOut)
def ingest_event(payload: SaleEventIn, db: Session = Depends(get_db)):
    """
    Simulates a POS terminal sending a sale event to the backend.
    """
    event = SaleEvent(
        terminal_id=payload.terminal_id,
        receipt_id=payload.receipt_id,
        amount=payload.amount,
        currency=payload.currency,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    logger.info(
        f"[INGEST] terminal_id={event.terminal_id} "
        f"receipt_id={event.receipt_id} "
        f"amount={event.amount} currency={event.currency} "
        f"status={event.status}"
    )

    return event


@app.get("/events", response_model=List[SaleEventOut])
def list_events(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Returns all events, optionally filtered by status (PENDING/PROCESSED).
    """
    query = db.query(SaleEvent)
    if status:
        status_filter = status.upper()
        query = query.filter(SaleEvent.status == status_filter)
    else:
        status_filter = "ALL"

    events = query.order_by(SaleEvent.created_at.desc()).all()

    logger.info(
        f"[LIST_EVENTS] count={len(events)} status_filter={status_filter}"
    )

    return events


@app.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    """
    Simple monitoring endpoint with counts by status.
    """
    total = db.query(SaleEvent).count()
    pending = db.query(SaleEvent).filter(SaleEvent.status == "PENDING").count()
    processed = db.query(SaleEvent).filter(SaleEvent.status == "PROCESSED").count()

    logger.info(
        f"[METRICS] total={total} pending={pending} processed={processed}"
    )

    return {
        "total_events": total,
        "pending_events": pending,
        "processed_events": processed,
    }

@app.post("/sync")
def sync_pending_events(db: Session = Depends(get_db)):
    """
    Simulates a background worker that processes all PENDING events
    and marks them as PROCESSED.
    """
    pending_events = db.query(SaleEvent).filter(SaleEvent.status == "PENDING").all()
    processed_count = 0

    for event in pending_events:
        event.status = "PROCESSED"
        processed_count += 1

    db.commit()

    logger.info(f"[SYNC] processed={processed_count} pending_before={len(pending_events)}")

    return {
        "processed_events": processed_count,
        "message": "Sync completed"
    }
