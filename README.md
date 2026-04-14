# 🛡️ Project AccessDenied | Cyber-Physical SOC Dashboard

An enterprise-grade Security Operations Center (SOC) platform designed to monitor and protect cyber-physical systems by correlating IT network threats, OT process anomalies, and perimeter intrusions in real time.

---

## 🚀 Key Highlights

- Unified monitoring of **IT (network)** and **OT (industrial process)** environments  
- Real-time anomaly detection using **unsupervised machine learning models**  
- High-fidelity threat detection via **honeypot-based intrusion trapping**  
- Instant, auditable incident response using deterministic edge-logic  

---

## 🧠 System Overview

AccessDenied integrates three security layers into a single platform:

1. **IT Layer (Network Security)**  
   Detects high-speed attacks such as DDoS and port scans  

2. **OT Layer (Process Security)**  
   Identifies anomalies in physical systems like pumps and tanks  

3. **Perimeter Layer (Deception Security)**  
   Uses a honeypot to trap and flag malicious interactions  

---

## ⚙️ How It Works

1. The backend simulates a **real-time digital twin** of an industrial system  
2. Incoming data is processed through two ML pipelines:
   - Isolation Forest → detects network anomalies  
   - One-Class SVM → detects process anomalies  
3. A **honeypot system** flags any external intrusion attempts with zero false positives  
4. The frontend correlates all signals using **deterministic edge-logic**  
5. The SOC dashboard displays **real-time alerts and actionable responses**  

---

## 🛠️ Tech Stack

**Frontend:** React, Vite, Tailwind CSS, Recharts  
**Backend:** FastAPI, Python  
**Machine Learning:** Scikit-Learn, Pandas  
**Security Simulation:** Honeypot (Conpot/Docker), Zeek NSM logs  
**Data Source:** Simulated SCADA + network telemetry (Digital Twin)  

---

## 🧩 Core Features

### 🤖 Dual Anomaly Detection Engine
- **Isolation Forest (IT Layer):** Detects network intrusions in high-dimensional data  
- **One-Class SVM (OT Layer):** Uses time-series smoothing to identify process anomalies  

### 🎯 Honeypot-Based Intrusion Detection
- Simulates vulnerable industrial endpoints  
- Flags all interactions as **high-confidence threats**  
- Eliminates false positives from background noise  

### ⚡ Deterministic Edge-Logic Engine
- Replaces LLM-based reasoning with **rule-based decision logic**  
- Instantly correlates IT, OT, and perimeter signals  
- Outputs **predefined, auditable incident responses**  

### 📡 Digital Twin Simulation
- Streams real-time industrial telemetry  
- Simulates SCADA systems without physical hardware  
- Enables safe testing of cyber-physical attacks  

---

## 📊 Performance Overview

| Layer        | Model             | Key Strength              |
|-------------|------------------|---------------------------|
| IT Network  | Isolation Forest | High recall for fast attacks |
| OT Process  | One-Class SVM    | Detects slow, subtle anomalies |

> Models are optimized for **high recall**, prioritizing detection of critical threats over false negatives.

---

## 📸 Screenshots (Add Yours Here)
<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/f1845f65-e8ea-427f-beba-615dfbda0602" />
<img width="1919" height="1026" alt="image" src="https://github.com/user-attachments/assets/1968d9e4-c409-4856-be30-ca7db6667ae2" />
<img width="1919" height="1032" alt="image" src="https://github.com/user-attachments/assets/fad9e471-254b-4de8-8831-567cef0d6683" />
<img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/db83fc46-a414-4728-8637-5d11e7afa678" />

---

## 🏗️ System Architecture (Add Diagram)

Recommended diagram flow:

Telemetry → FastAPI Backend → ML Models → Edge Logic → React Dashboard


---

## 🚀 Getting Started

## 1. Clone the Repository
git clone https://github.com/swastigupta8/Project-AccessDenied.git
cd Project-AccessDenied
## 2. Setup Backend
python -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)
pip install fastapi uvicorn pandas scikit-learn requests
uvicorn main:app --reload
## 3. Setup Frontend
cd project-frontend
npm install
npm run dev

## 🎯 Impact

AccessDenied addresses a critical gap in modern infrastructure security by:

Eliminating alert fatigue through high-confidence detection
Bridging the gap between IT and OT security systems
Enabling real-time, automated incident response for critical infrastructure

## 👩‍💻 Author

Swasti Gupta
Computer Science Undergraduate, Manipal Institute of Technology
