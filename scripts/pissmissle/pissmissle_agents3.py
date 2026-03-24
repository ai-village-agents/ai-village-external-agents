import requests
import json
import time

base_url = "https://api.pissmissle.fun"

print("--- Agents 1-20 ---")
# Try iterating through IDs 1-20
for i in range(1, 21):
    try:
        resp = requests.get(f"{base_url}/api/forum/agents/{i}")
        if resp.status_code == 200:
            print(f"Agent ID {i}: {resp.json().get('username')} ({resp.json().get('displayName')})")
        elif resp.status_code != 404:
            print(f"Agent ID {i}: Status {resp.status_code}")
    except Exception as e:
        print(f"Error {i}: {e}")
    time.sleep(0.1)

