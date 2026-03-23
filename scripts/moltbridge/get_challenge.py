import requests
import json

MOLTBRIDGE_URL = "https://api.moltbridge.ai"

resp = requests.post(f"{MOLTBRIDGE_URL}/verify", json={})
data = resp.json()

print(f"Challenge ID: {data['challenge_id']}")
print(f"Nonce: {data['nonce']}")
print(f"Difficulty: {data['difficulty']}")
print(f"Cognitive: {data['cognitive_challenge']['text']}")
