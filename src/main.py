from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import os

# Updated title for that cybersecurity aesthetic
app = FastAPI(title="Access Denied")

# This allows Arisha's frontend to access your local server without being blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Brain
MODEL_PATH = '../models/batadal_ocsvm.pkl'
SCALER_PATH = '../models/batadal_scaler.pkl'
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# --- ENDPOINT A: FOR TESTING ---
@app.post("/predict")
async def predict_single_point(data: dict):
    """Used by the team to test single rows via Swagger UI"""
    try:
        df = pd.DataFrame([data])
        df.columns = df.columns.str.strip().str.upper()
        
        cols_to_drop = ['DATETIME', 'ATT_FLAG', 'ATTACK']
        features = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

        scaled = scaler.transform(features)
        raw_score = model.decision_function(scaled)[0]
        
        # Confidence logic for the dashboard
        confidence = 1 / (1 + np.exp(raw_score))
        risk = "Low"
        if confidence >= 0.75: risk = "High"
        elif confidence >= 0.40: risk = "Medium"

        return {
            "prediction": "ANOMALY" if raw_score < 0 else "NORMAL",
            "confidence_score": round(float(confidence), 4),
            "risk_level": risk,
            "raw_score": round(float(raw_score), 4)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- ENDPOINT B: FOR DASHBOARD FEED ---
@app.get("/dashboard/feed")
async def get_dashboard_feed():
    """Arisha calls this to populate the live alerts table"""
    file_path = '../data/dashboard_feed.csv'
    if not os.path.exists(file_path):
        return {"error": "Run detect.py first to generate feed."}
    
    df = pd.read_csv(file_path)
    return df.tail(100).to_dict(orient="records")

# --- ENDPOINT C: FOR CONFUSION MATRIX ---
@app.get("/dashboard/matrix")
async def get_matrix():
    """Arisha calls this to draw the accuracy heatmap"""
    file_path = '../data/full_risk_matrix.csv'
    if not os.path.exists(file_path):
        return {"error": "Run benchmark.py first to generate matrix data."}
    
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")