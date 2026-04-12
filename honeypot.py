import socket
import requests

# CONFIGURATION
HONEYPOT_IP = "0.0.0.0"  # Listen on all network interfaces
HONEYPOT_PORT = 8080      # Mimic a web server port
BACKEND_URL = "http://127.0.0.1:8000/api/honeypot/alert"

def start_honeypot():
    # Create a socket to listen for intruders
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HONEYPOT_IP, HONEYPOT_PORT))
    server.listen(5)
    
    print(f"[*] Honeypot Active! Trapping intruders on port {HONEYPOT_PORT}...")

    while True:
        client, addr = server.accept()
        attacker_ip = addr[0]
        print(f"🚨 INTRUSION DETECTED! Attacker IP: {attacker_ip}")

        # Send the alert to your FastAPI backend
        try:
            payload = {"attacker_ip": attacker_ip, "port": HONEYPOT_PORT}
            requests.post(BACKEND_URL, json=payload)
        except Exception as e:
            print(f"Failed to alert backend: {e}")

        # Send a fake "Success" message to keep the hacker interested
        client.send(b"HTTP/1.1 200 OK\n\nWelcome to the Admin Portal. Please login.")
        client.close()

if __name__ == "__main__":
    start_honeypot()