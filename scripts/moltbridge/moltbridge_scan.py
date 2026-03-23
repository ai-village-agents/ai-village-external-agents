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
    
    payload_to_sign = f"{method.upper()}:{path}:{timestamp}:{body_hash}".encode('utf-8')
    
    signature_bytes = private_key.sign(payload_to_sign)
    signature_b64url = base64.urlsafe_b64encode(signature_bytes).decode('utf-8').rstrip('=')
    
    return timestamp, signature_b64url

def check_target(target):
    private_key = load_private_key("moltbridge_priv.pem")
    method = "POST"
    path = "/discover-broker"
    body_dict = {"target_identifier": target}
    
    timestamp, signature = sign_request(private_key, method, path, body_dict)
    
    auth_header = f"MoltBridge-Ed25519 {AGENT_ID}:{timestamp}:{signature}"
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }
    
    url = f"{MOLTBRIDGE_URL}{path}"
    resp = requests.post(url, headers=headers, json=body_dict)
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get("path_found"):
            print(f"[FOUND] {target}: {json.dumps(data.get('results', []), indent=2)}")
        else:
            print(f"[NOT FOUND] {target}")
    else:
        print(f"[ERROR] {target}: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    targets = [
        "weaver",
        "sage",
        "sageandweaver",
        "weaver-aiciv",
        "weaver-aiciv.bsky.social",
        "a-c-gee",
        "echo-civ",
        "vector-civ",
        "bob",
        "gptme",
        "agentcheck",
        "chatgpt",
        "legaleasy",
        "policycheck",
        "pixelfamiliar",
        "clankops",
        "survivorforge",
        "stromfee",
        "stromfee.ai",
        "kai",
        "aion",
        "ai-village-gpt54-moltbridge"
    ]
    
    print("Scanning targets on MoltBridge...")
    for target in targets:
        check_target(target)
        time.sleep(1) # Be nice to the API
