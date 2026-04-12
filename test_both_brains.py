import joblib
import pandas as pd

print("=== INITIATING SOC SYSTEM TEST ===")
print("1. Waking up both AI Brains...")
process_model = joblib.load('process_brain.pkl')
network_model = joblib.load('network_brain.pkl')

print("2. Fetching live telemetry (Grabbing Row 0 from both datasets)...")

# ==========================================
# PREPPING PROCESS DATA (BATADAL)
# ==========================================
df_process = pd.read_csv('BATADAL_Train_1.csv', nrows=5)
for col in ['DATETIME', 'ATT_FLAG', 'label']:
    if col in df_process.columns:
        df_process = df_process.drop(col, axis=1)

# This is the line that went missing!
live_process_packet = df_process.select_dtypes(include=['float64', 'int64']).fillna(0).iloc[[0]]

# ==========================================
# PREPPING NETWORK DATA (TON_IoT Windows 10)
# ==========================================
df_network = pd.read_csv('Train_Test_Windows_10.csv', nrows=5)

# The Magic Fix: Ask the AI what columns it wants
expected_columns = network_model.feature_names_in_

for col in expected_columns:
    if col not in df_network.columns:
        df_network[col] = 0

live_network_packet = df_network[expected_columns].fillna(0).iloc[[0]]

print("\n==========================================")
print("   PAGE 1: PROCESS MONITOR (OCSVM)")
print("==========================================")
process_score = process_model.decision_function(live_process_packet)[0]
print(f"Raw Math Score: {process_score:.4f}")

if process_score < -5.0:
    print("🚨 STATUS: HIGH CONFIDENCE (Physics Breach Detected!)")
elif process_score < 0.0:
    print("⚠️ STATUS: MEDIUM CONFIDENCE (Suspicious telemetry logged)")
else:
    print("✅ STATUS: LOW / NORMAL (Water systems operating safely)")

print("\n==========================================")
print("   PAGE 2: NETWORK MONITOR (Isolation Forest)")
print("==========================================")
network_score = network_model.decision_function(live_network_packet)[0]
print(f"Raw Math Score: {network_score:.4f}")

if network_score < -0.15:
    print("🚨 STATUS: HIGH CONFIDENCE (Network Attack Detected!)")
elif network_score < 0.0:
    print("⚠️ STATUS: MEDIUM CONFIDENCE (Network scan detected)")
else:
    print("✅ STATUS: LOW / NORMAL (Network traffic looks clean)")
print("\n=== SYSTEM TEST COMPLETE ===")