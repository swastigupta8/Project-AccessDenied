"""
Live model inference for AccessDenied.

Previously main.py streamed a CSV that already had AI_THREAT_LEVEL /
AI_THREAT_SCORE columns baked in offline — the "AI" in the demo was just
replaying pre-computed labels. This module actually loads the trained
sklearn models and runs .predict() / .decision_function() on each row
at request time.

Honesty note (keep this in mind for interviews / resume wording):
the *rows themselves* are replayed from held-out CSV data, not captured
from a live network — there's no real sensor feeding this. What's real
is that the model inference happens live, on each request, not
pre-baked. That distinction matters and you should be able to explain
it if asked.
"""
import os
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_network_model = joblib.load(os.path.join(BASE_DIR, "models", "network_brain.pkl"))
_process_model = joblib.load(os.path.join(BASE_DIR, "models", "process_brain.pkl"))

_network_features = list(_network_model.feature_names_in_)
_process_features = list(_process_model.feature_names_in_)

_network_df = pd.read_csv(os.path.join(BASE_DIR, "data", "windows10_live.csv"))
_process_df = pd.read_csv(os.path.join(BASE_DIR, "data", "batadal_live.csv"))
_process_df.columns = _process_df.columns.str.strip().str.upper()
_process_features = [c.upper() for c in _process_features]

_network_cursor = 0
_process_cursor = 0


def _score_to_confidence(raw_score: float) -> float:
    # OneClassSVM/IsolationForest: negative decision_function => anomaly.
    # Sigmoid maps that to a 0..1 "confidence this is an anomaly" score.
    return float(1 / (1 + np.exp(raw_score)))


def _risk_level(confidence: float) -> str:
    if confidence < 0.40:
        return "Low"
    elif confidence < 0.75:
        return "Medium"
    return "High"


def next_network_prediction() -> dict:
    """Runs IsolationForest inference live on the next held-out network row."""
    global _network_cursor
    row = _network_df.iloc[_network_cursor % len(_network_df)]
    _network_cursor += 1

    x = pd.DataFrame([row[_network_features].fillna(0)])
    pred = _network_model.predict(x)[0]  # 1 = normal, -1 = anomaly
    raw_score = float(_network_model.decision_function(x)[0])
    confidence = _score_to_confidence(raw_score)

    return {
        "model": "network_isolation_forest",
        "prediction": "Normal" if pred == 1 else "ANOMALY",
        "raw_score": round(raw_score, 4),
        "confidence": round(confidence, 4),
        "risk_level": _risk_level(confidence),
        "label_hint": str(row.get("label", "n/a")),  # ground-truth label if present, for your own debugging
    }


def next_process_prediction() -> dict:
    """Runs OneClassSVM inference live on the next held-out BATADAL row."""
    global _process_cursor
    row = _process_df.iloc[_process_cursor % len(_process_df)]
    _process_cursor += 1

    x = pd.DataFrame([row[_process_features].fillna(0)])
    pred = _process_model.predict(x)[0]
    raw_score = float(_process_model.decision_function(x)[0])
    confidence = _score_to_confidence(raw_score)

    return {
        "model": "process_ocsvm",
        "prediction": "Normal" if pred == 1 else "ANOMALY",
        "raw_score": round(raw_score, 4),
        "confidence": round(confidence, 4),
        "risk_level": _risk_level(confidence),
        "raw_data": {"L_T1": float(row.get("L_T1", 0)), "F_PU1": float(row.get("F_PU1", 0))},
    }
