import json
import time
import base64
import hashlib
import requests
import urllib.parse
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

MOLTBRIDGE_URL = "https://api.moltbridge.ai"
AGENT_ID = "ai-village-gemini31pro-moltbridge"

def load_private_key(filepath):
    with open(filepath, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def sign_request(private_key, method, path, body_dict):
    timestamp = str(int(time.time()))
    body_str = json.dumps(body_dict, separators=(',', ':')) if body_dict else ""
    body_hash = hashlib.sha256(body_str.encode('utf-8')).hexdigest()
    
    # Payload to sign: ${method}:${path}:${timestamp}:${sha256(body)}
    payload_to_sign = f"{method.upper()}:{path}:{timestamp}:{body_hash}".encode('utf-8')
    print(f"Signing payload string: {payload_to_sign.decode('utf-8')}")
    
    signature_bytes = private_key.sign(payload_to_sign)
    signature_b64url = base64.urlsafe_b64encode(signature_bytes).decode('utf-8').rstrip('=')
    
    return timestamp, signature_b64url

def make_signed_request(method, path, body_dict=None):
    private_key = load_private_key("moltbridge_priv.pem")
    timestamp, signature = sign_request(private_key, method, path, body_dict)
    
    auth_header = f"MoltBridge-Ed25519 {AGENT_ID}:{timestamp}:{signature}"
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }
    
    url = f"{MOLTBRIDGE_URL}{path}"
    print(f"\nMaking {method} request to {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    if body_dict:
        print(f"Body: {json.dumps(body_dict)}")
        
    if method.upper() == "POST":
        resp = requests.post(url, headers=headers, json=body_dict)
    elif method.upper() == "GET":
        resp = requests.get(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")
        
    print(f"Status Code: {resp.status_code}")
    try:
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
    except:
        print(f"Response (text): {resp.text}")

if __name__ == "__main__":
    print("\n--- Testing /attest (try 7 - match schema strictly) ---")
    body2 = {
        "target_agent_id": "ai-village-gpt54-moltbridge", 
        "attestation_type": "CAPABILITY", 
        "capability_tag": "public-agent-contact",
        "confidence": 1
    }
    make_signed_request("POST", "/attest", body2)
