import requests
import json

resp = requests.get("https://api.moltbridge.ai/.well-known/agent.json")
try:
    print(json.dumps(resp.json(), indent=2))
except:
    print(resp.text)
