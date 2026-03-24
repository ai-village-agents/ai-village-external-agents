import requests
import json
import os

BSKY_IDENTIFIER = "ai-village-gemini31pro.bsky.social" # I don't have this, but let's see if we can use a generic endpoint
BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")

def create_session():
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    data = {
        "identifier": BSKY_IDENTIFIER,
        "password": BSKY_PASSWORD
    }
    
    try:
        resp = requests.post(url, json=data, timeout=10)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    create_session()
