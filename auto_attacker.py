import time
import random
import requests

# This points to your FastAPI honeypot alert endpoint
BACKEND_URL = "http://127.0.0.1:8000/api/honeypot/alert"

print("🔥 Auto-Attacker Initialized. Firing fake intrusions...")

while True:
    # Generate a scary-looking random IP address
    fake_ip = f"{random.randint(45, 210)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    payload = {
        "attacker_ip": fake_ip, 
        "port": 8080
    }
    
    try:
        requests.post(BACKEND_URL, json=payload)
        print(f"🚨 Sent fake probe from {fake_ip} to Honeypot!")
    except Exception as e:
        print("Backend offline. Ensure uvicorn is running.")
    
    # Wait randomly between 3 to 10 seconds before the next attack
    time.sleep(random.randint(3, 10))