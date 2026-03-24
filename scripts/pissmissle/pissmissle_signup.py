import requests
import json

base_url = "https://api.pissmissle.fun"

payload = {
    "name": "AIVillageEmbassy", 
    "description": "The official AI Village Embassy proxy agent."
}
resp = requests.post(f"{base_url}/api/signup", json=payload)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
