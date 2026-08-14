import time
import random
from datetime import datetime, timezone

import pandas as pd
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import init_db, get_session, HoneypotEvent, InferenceLog
import inference
import soc_analyst

app = FastAPI(title="AccessDenied SOC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# ==========================================
# HONEYPOT — now persisted to SQLite instead of an in-memory list
# ==========================================
def get_db():
    db = next(get_session())
    try:
        yield db
    finally:
        pass


@app.post("/api/honeypot/alert")
async def honeypot_alert(data: dict, db: Session = Depends(get_db)):
    """Receives alerts from auto_attacker.py or actual intruders and persists them."""
    event = HoneypotEvent(
        attacker_ip=data.get("attacker_ip", "Unknown IP"),
        port=data.get("port", 8080),
        status="CRITICAL",
        event_type="DECEPTION_TRIGGER",
    )
    db.add(event)
    db.commit()
    print(f"HONEYPOT ACTIVATED by {event.attacker_ip}")
    return {"status": "Logged"}


@app.get("/api/honeypot/logs")
async def get_honeypot_logs(db: Session = Depends(get_db)):
    """Returns persisted intrusion events (survives restarts now)."""
    events = db.query(HoneypotEvent).order_by(HoneypotEvent.created_at.desc()).limit(200).all()
    return [
        {
            "attacker_ip": e.attacker_ip,
            "port": e.port,
            "status": e.status,
            "type": e.event_type,
            "timestamp": e.created_at.isoformat(),
        }
        for e in events
    ]


# ==========================================
# PROCESS AI STREAM — live OneClassSVM inference, not a pre-labeled CSV replay
# ==========================================
@app.get("/api/stream")
async def stream_data(db: Session = Depends(get_db)):
    """Runs the trained One-Class SVM live on the next held-out BATADAL row."""
    result = inference.next_process_prediction()

    db.add(InferenceLog(
        model_name=result["model"],
        prediction=result["prediction"],
        raw_score=result["raw_score"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
    ))
    db.commit()

    status = "HIGH" if result["risk_level"] == "High" else "MEDIUM" if result["risk_level"] == "Medium" else "LOW"
    return {
        "status": status,
        "threat_confidence": round(result["confidence"] * 100),
        "color": "red" if status == "HIGH" else "yellow" if status == "MEDIUM" else "green",
        "raw_data": result["raw_data"],
        "model_prediction": result["prediction"],
    }


# ==========================================
# NETWORK AI STREAM — live IsolationForest inference
# ==========================================
@app.get("/api/network/stream")
async def network_stream(db: Session = Depends(get_db)):
    """Runs the trained Isolation Forest live on the next held-out Windows telemetry row."""
    result = inference.next_network_prediction()

    db.add(InferenceLog(
        model_name=result["model"],
        prediction=result["prediction"],
        raw_score=result["raw_score"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
    ))
    db.commit()

    status = "HIGH" if result["risk_level"] == "High" else "MEDIUM" if result["risk_level"] == "Medium" else "LOW"
    return {
        "status": status,
        "threat_confidence": round(result["confidence"] * 100),
        "color": "red" if status == "HIGH" else "yellow" if status == "MEDIUM" else "green",
        "model_prediction": result["prediction"],
    }


# ==========================================
# SOC ANALYST — real Claude API call (falls back honestly if no key set)
# ==========================================
@app.post("/api/soc-analyst")
async def generate_soc_report(data: dict):
    process_status = data.get("process_status", "LOW")
    network_status = data.get("network_status", "LOW")
    hits = data.get("honeypot_hits", 0)
    return soc_analyst.generate_report(process_status, network_status, hits)


# ==========================================
# SIMULATED NETWORK TELEMETRY FEED
# Honest label: this is synthetic demo data, NOT parsed from a real Zeek
# sensor. A real integration would require live packet capture
# infrastructure, which is out of scope for a portfolio deployment.
# ==========================================
@app.get("/api/network/simulated-telemetry")
async def get_simulated_telemetry():
    """Synthetic network event feed for dashboard visuals. NOT real Zeek output."""
    protocols = ["TCP", "UDP", "ICMP", "DNS"]
    states = ["S0", "REJ", "RSTO", "OTH"]
    logs = []
    for _ in range(random.randint(3, 5)):
        logs.append({
            "ts": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "id.orig_h": f"192.168.1.{random.randint(20, 250)}",
            "id.orig_p": random.randint(1024, 65535),
            "proto": random.choice(protocols),
            "conn_state": random.choice(states),
            "note": random.choice([
                "Bad TCP checksum", "DNS query with no response",
                "Suspicious payload size", "Multiple failed connections",
            ]),
            "simulated": True,
        })
    return logs
