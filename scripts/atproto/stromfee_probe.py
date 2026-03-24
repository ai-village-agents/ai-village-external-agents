import requests
import json
import time
from datetime import datetime

def check_stromfee():
    url = "https://stromfee.ai/api/frequency.php"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                current = data.get("current", {})
                freq = current.get("frequency")
                status = current.get("status")
                dt = datetime.fromtimestamp(current.get("timestamp", 0))
                print(f"[Stromfee.ai] Status: {status} | Freq: {freq} Hz | Time: {dt}")
                return data
            else:
                print(f"[Stromfee.ai] API returned success: false")
        else:
            print(f"[Stromfee.ai] HTTP {resp.status_code}")
    except Exception as e:
        print(f"[Stromfee.ai] Error: {e}")
    return None

if __name__ == "__main__":
    check_stromfee()
