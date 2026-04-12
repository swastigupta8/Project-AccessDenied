# 🛡️ Project AccessDenied

**An autonomous Cyber-Physical Security Operations Center (SOC) triangulating IT network threats, OT process anomalies, and perimeter deception in real-time.**

Project AccessDenied is an enterprise-grade SOC dashboard engineered to protect Cyber-Physical Systems (CPS) and critical infrastructure (e.g., Water Treatment Plants). Recognizing the vulnerability of modern industrial networks, this platform correlates threat intelligence across three distinct attack vectors to eliminate alert fatigue and detect zero-day anomalies with zero latency.

---

## ⚡ Core Features

* **ICS/SCADA Process Anomaly Engine (OT Layer):** Utilizes a **One-Class Support Vector Machine (SVM)** with time-series smoothing (7-hour rolling averages) to detect slow, sustained physical attacks on water pumps and tanks without triggering false alarms on benign pressure spikes.
* **IT Network Anomaly Engine (IT Layer):** Deploys an **Isolation Forest** algorithm trained on a "Pure Normal" filtered baseline to detect high-speed, highly dimensional network intrusions (DDoS, Port Scans) in real-time.
* **Active Perimeter Deception (Honeypot):** A simulated Docker/Conpot ICS honeypot exposes vulnerable ports to the internet. Any interaction is immediately flagged as a high-fidelity, zero-false-positive critical alert.
* **Deep Packet Inspection (Zeek NSM):** A simulated Zeek Network Security Monitor streams continuous `weird.log` outputs, providing granular packet-level context during IT anomalies.
* **Autonomous Edge-Logic Intelligence:** Bypasses slow, hallucination-prone LLM APIs by utilizing a deterministic React edge-logic engine. It instantaneously triangulates vector states to render predefined, auditable incident response directives.

---

## 🏗️ System Architecture

* **Frontend (UI/UX):** React, Vite, Tailwind CSS v4, Recharts.
* **Backend (API & ML Pipeline):** Python, FastAPI, Scikit-Learn, Pandas.
* **Data Layer:** Software-in-the-Loop (SIL) Digital Twin streaming historical BATADAL (Process) and Windows 10 (Network) telemetry.

---

## 🚀 How to Run the Project locally

### Prerequisites
* **Python 3.8+** (For the machine learning backend and API)
* **Node.js 18+** (For the React frontend)

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/AccessDenied-v2.git](https://github.com/YourUsername/AccessDenied-v2.git)
cd AccessDenied
```

### 2. Start the FastAPI Backend
The backend serves the ML inference engine, the digital twin data stream, and the Honeypot trap.

```bash
# Navigate to the backend directory (if separated, or stay in root)
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pandas scikit-learn requests

# Start the backend server
uvicorn main:app --reload
```
*The backend is now running at `http://127.0.0.1:8000`*

### 3. Start the React Frontend
Open a **new, separate terminal window**, leave the backend running, and execute:

```bash
# Navigate to the frontend directory
cd project-frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*The SOC Dashboard is now live. Click the Localhost link provided in the terminal to open it in your browser.*

### 4. Triggering Perimeter Attacks (Optional)
To test the Honeypot UI and see the deception trap catch live intrusions, open a **third terminal window** and run the automated attacker script:

```bash
python auto_attacker.py
```
*Watch the frontend Honeypot radar instantly light up with critical alerts as the script probes your exposed ports.*

---

## 📊 Performance Benchmarks
Our unsupervised, edge-deployable models were calibrated to prioritize **Recall** (minimizing False Negatives in life-or-death infrastructure scenarios) over raw academic Accuracy.

| Vector | Algorithm | F1 Score | Recall |
| :--- | :--- | :--- | :--- |
| **IT Network** | Isolation Forest | 77.11% | 83.11% |
| **OT Process** | One-Class SVM | 62.94% | 61.64% |



## 🎯 What It Does (The Business Value)
Modern critical infrastructure—like water treatment plants and power grids—operates in two overlapping worlds: the digital IT network (computers, servers) and the physical OT process (valves, pumps). Traditionally, these are monitored by separate teams, leading to blind spots.

AccessDenied unifies these worlds into a single, autonomous command center.

Eliminates Alert Fatigue: By deploying an active Honeypot decoy, the system traps background internet noise (like automated bot scanners). This allows the internal AI to focus strictly on genuine, targeted attacks without overwhelming the SOC analyst with false alarms.

Correlates Cyber-Physical Threats: It instantly answers the most critical question in infrastructure security: "Is this just a network glitch, or is a hacker actively manipulating our physical water pumps?"

Automates Triage: Instead of forcing an analyst to interpret raw graphs during a crisis, the system autonomously translates anomalies into immediate, actionable mitigation steps (e.g., "Sever IT/OT network bridges" or "Transition valves to manual override").

## ⚙️ How It Works (Under the Hood)
The platform operates on a decoupled, high-throughput data pipeline that processes information in four continuous stages:

**Step 1: Data Ingestion (The Digital Twin)**
Because deploying physical Programmable Logic Controllers (PLCs) at a hackathon is unfeasible, the FastAPI backend acts as a Software-in-the-Loop (SIL) Digital Twin. It continuously streams complex SCADA telemetry (tank levels, pump statuses) and deep-packet IT network logs, simulating a live industrial environment with zero latency.

**Step 2: Dual-Engine Machine Learning Inference**
The backend routes the incoming telemetry through two specialized, unsupervised AI models:

The IT Engine (Isolation Forest): Slices through highly dimensional network traffic to isolate fast-moving digital anomalies, such as DDoS attempts or port scans.

The OT Engine (One-Class SVM): Applies a 7-hour time-series smoothing window to the physical water plant data. It profiles the "steady state" of the plant to detect slow, methodical physical tampering that traditional threshold alarms miss.

**Step 3: Perimeter Deception & NSM Logging**
Simultaneously, the backend manages a simulated Conpot/Docker ICS Honeypot on port 8080 and streams simulated Zeek Network Security Monitor (weird.log) outputs. Any IP address that interacts with the Honeypot is instantly logged as a high-fidelity critical threat, bypassing the ML models entirely.

**Step 4: Deterministic Edge-Logic (The UI)**
The React frontend asynchronously polls these backend states. Instead of relying on slow, hallucination-prone Large Language Models (LLMs) to write incident reports, the frontend utilizes an Autonomous Edge-Logic Engine. Using strict Boolean rules, the dashboard instantaneously triangulates the IT, OT, and Deception vectors to shift UI colors and render predefined, auditable threat intelligence with zero API latency.
