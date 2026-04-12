from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import random

app = FastAPI()

# --- CORS SETUP ---
# This allows your React frontend to talk to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- GLOBAL VARIABLES ---
honeypot_events = []
current_row = 0

# --- LOAD PROCESS DATA FOR STREAMING ---
try:
    demo_data = pd.read_csv('LABELED_Process_Test.csv').to_dict('records')
    print(f"✅ Loaded {len(demo_data)} rows of Process Data for streaming.")
except Exception as e:
    print("⚠️ Warning: LABELED_Process_Test.csv not found. Process stream will be empty.", e)
    demo_data = []

# ==========================================
# ENDPOINT 1 & 2: THE HONEYPOT DECEPTION TRAP
# ==========================================
@app.post("/api/honeypot/alert")
async def honeypot_alert(data: dict):
    """Receives alerts from auto_attacker.py or actual intruders"""
    event = {
        "attacker_ip": data.get("attacker_ip", "Unknown IP"),
        "port": data.get("port", 8080),
        "status": "CRITICAL",
        "type": "DECEPTION_TRIGGER"
    }
    honeypot_events.append(event)
    print(f"🔥 HONEYPOT ACTIVATED by {event['attacker_ip']}")
    return {"status": "Logged"}

@app.get("/api/honeypot/logs")
async def get_honeypot_logs():
    """Sends the list of intruders to the React Dashboard"""
    return honeypot_events

# ==========================================
# ENDPOINT 3: THE PROCESS AI DATA STREAMER
# ==========================================
@app.get("/api/stream")
async def stream_data():
    """Streams the labeled water plant CSV data row-by-row to React"""
    global current_row
    if not demo_data:
        return {"error": "No labeled CSV found."}
    
    # Get current row and loop back to start if at the end
    row = demo_data[current_row]
    current_row = (current_row + 1) % len(demo_data) 
    
    status = row.get("AI_THREAT_LEVEL", "LOW")
    score = float(row.get("AI_THREAT_SCORE", 5))
    
    # Format the payload for the React Gauges
    return {
        "status": status,
        "threat_confidence": min(abs(int(score * 2)), 100) if status != "LOW" else 5,
        "color": "red" if status == "HIGH" else "yellow" if status == "MEDIUM" else "green",
        "raw_data": {"L_T1": row.get("L_T1", 0), "F_PU1": row.get("F_PU1", 0)}
    }

# ==========================================
# ENDPOINT 4: GEMINI AI SOC ANALYST
# ==========================================
import time

@app.post("/api/soc-analyst")
async def generate_soc_report(data: dict):
    """Simulates an AI SOC Analyst dynamically analyzing the telemetry"""
    
    # 1. Grab the real live data from your React dashboard
    process_status = data.get('process_status', 'LOW')
    network_status = data.get('network_status', 'LOW')
    hits = data.get('honeypot_hits', 0)
    
    # 2. Add a realistic 1.5-second "thinking" delay
    time.sleep(1.5)
    
    # 3. Dynamically generate the report based on the real metrics
    if hits > 0 and (process_status == "HIGH" or network_status == "HIGH"):
         report = f"CRITICAL INCIDENT: Multi-vector cyber-physical attack detected. The deception trap has captured {hits} unauthorized external probes, correlating with a {process_status} anomaly in the ICS water pump telemetry. Immediate action required: Sever external IT/OT network bridges and transition water pumps to manual override."
         
    elif hits > 0:
         report = f"ELEVATED RISK: Perimeter breach attempt in progress. The honeypot decoy has absorbed {hits} intrusion attempts, but internal IT and Process telemetry currently remain secure. Recommendation: Block the offending external IP addresses at the firewall and maintain heightened monitoring."
         
    elif process_status == "HIGH" or network_status == "HIGH":
         report = f"WARNING: Internal anomaly detected without perimeter breach. Network telemetry indicates a {network_status} threat, while physical process systems show a {process_status} threat. Recommendation: Investigate potential insider threat or localized hardware failure. Isolate affected subnets."
         
    else:
         report = "SYSTEM NOMINAL: All Industrial Control Systems (ICS) and IT network telemetry are operating within established baselines. The deception trap reports zero unauthorized intrusions. Posture: Continue standard automated monitoring."
         
    return {"report": report}

import random

@app.get("/api/zeek/logs")
async def get_zeek_logs():
    """Simulates a Zeek Network Sensor outputting weird.log entries"""
    protocols = ["TCP", "UDP", "ICMP", "DNS"]
    states = ["S0", "REJ", "RSTO", "OTH"]
    
    # Generate 3-5 random Zeek logs
    logs = []
    for _ in range(random.randint(3, 5)):
        logs.append({
            "ts": pd.Timestamp.now().strftime("%H:%M:%S"),
            "id.orig_h": f"192.168.1.{random.randint(20, 250)}",
            "id.orig_p": random.randint(1024, 65535),
            "proto": random.choice(protocols),
            "conn_state": random.choice(states),
            "note": random.choice(["Bad TCP checksum", "DNS query with no response", "Suspicious payload size", "Multiple failed connections"])
        })
    return logs