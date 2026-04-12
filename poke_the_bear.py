import socket

print("Attempting to connect to the Honeypot on Port 502...")

try:
    # Changed back to 502!
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('127.0.0.1', 502))
    print("SUCCESS! The Honeypot is alive and accepted our connection.")
    print("Look at your Docker terminal, Conpot should have logged this!")
    s.close()
except Exception as e:
    print(f"FAILED to connect. Error: {e}")