"""
Persistent storage for AccessDenied.

Replaces the in-memory `honeypot_events = []` list that previously reset
on every server restart. Uses SQLite (zero external DB server needed —
fine for a portfolio project; swap DATABASE_URL for Postgres if you ever
need multi-instance deployment).
"""
import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./accessdenied.db")

# check_same_thread=False is required for SQLite + FastAPI's threaded workers
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class HoneypotEvent(Base):
    __tablename__ = "honeypot_events"
    id = Column(Integer, primary_key=True, index=True)
    attacker_ip = Column(String, index=True)
    port = Column(Integer)
    status = Column(String, default="CRITICAL")
    event_type = Column(String, default="DECEPTION_TRIGGER")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class InferenceLog(Base):
    """Every live model prediction gets logged — gives you a real audit
    trail instead of ephemeral in-memory state, and lets the dashboard
    show trend history across restarts."""
    __tablename__ = "inference_log"
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)  # "network_isolation_forest" | "process_ocsvm"
    prediction = Column(String)              # "Normal" | "ANOMALY"
    raw_score = Column(Float)
    confidence = Column(Float)
    risk_level = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
