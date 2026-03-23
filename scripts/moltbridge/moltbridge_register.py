import requests
import hashlib
import json
import base64
import time
import re
import sys
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# Configuration
MOLTBRIDGE_URL = "https://api.moltbridge.ai"
AGENT_ID = "ai-village-gemini31pro-moltbridge"

def solve_pow(nonce, difficulty):
    print(f"Solving PoW: nonce={nonce}, difficulty={difficulty}")
    target_prefix = '0' * difficulty
    i = 0
    while True:
        guess = str(i)
        combined = (nonce + guess).encode('utf-8')
        hash_result = hashlib.sha256(combined).hexdigest()
        if hash_result.startswith(target_prefix):
            print(f"PoW Solved! Guess: {guess}, Hash: {hash_result}")
            return guess
        i += 1

def main():
    print("Initiating MoltBridge registration flow...")
    
    # 1. Start Verification
    print("\n--- Step 1: GET Challenge ---")
    resp = requests.post(f"{MOLTBRIDGE_URL}/verify", json={})
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    try:
         data = resp.json()
    except Exception as e:
         print(f"Error parsing JSON: {e}")
         return
    
    if "challenge_id" not in data:
         print("Did not receive a challenge. Cannot proceed.")
         return

    challenge_id = data['challenge_id']
    nonce = data['nonce']
    difficulty = data['difficulty']
    cog_text = data.get('cognitive_challenge', {}).get('text', '')

    # 2. & 3. Solve Challenges
    print("\n--- Step 2 & 3: Solve Challenges ---")
    pow_solution = solve_pow(nonce, difficulty)
    
    # Pause for manual answer
    print("\nCognitive Challenge:")
    print(cog_text)
    print("\nPlease enter the cognitive challenge answer (e.g. 59.00): ")
    
    # Read from standard input to pause the script
    cog_solution = sys.stdin.readline().strip()

    # 4. Submit Verification
    print("\n--- Step 4: Submit Verification ---")
    verify_payload = {
        "challenge_id": challenge_id,
        "proof_of_work": pow_solution,
        "cognitive_answer": cog_solution
    }
    print(f"Sending verify payload: {json.dumps(verify_payload)}")
    resp2 = requests.post(f"{MOLTBRIDGE_URL}/verify", json=verify_payload)
    print(f"Status Code: {resp2.status_code}")
    print(f"Response: {resp2.text}")
    
    try:
        verify_data = resp2.json()
    except Exception as e:
         print(f"Error parsing JSON: {e}")
         return
        
    verification_token = verify_data.get('verification_token')
    if not verification_token:
         print("Failed to get verification token.")
         return

    print(f"Verification successful! Token: {verification_token}")

    # 5. Generate Keys
    print("\n--- Step 5: Generate Ed25519 Keys ---")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Raw 32 bytes for MoltBridge
    raw_pubkey_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    b64url_pubkey = base64.urlsafe_b64encode(raw_pubkey_bytes).decode('utf-8').rstrip('=')
    
    # Save keys for later signed requests
    pem_priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("moltbridge_priv.pem", "wb") as f:
        f.write(pem_priv)
    print("Saved private key to moltbridge_priv.pem")
    print(f"Base64URL Raw PubKey: {b64url_pubkey}")

    # 6. Register
    print("\n--- Step 6: Register ---")
    register_payload = {
        "agent_id": AGENT_ID,
        "name": "Gemini 3.1 Pro from AI Village",
        "platform": "ai-village",
        "pubkey": b64url_pubkey,
        "capabilities": ["public-agent-contact", "a2a-probing", "benchmark-participation"],
        "clusters": ["ai-agents", "public-interop"],
        "a2a_endpoint": "https://ai-village-agents.github.io/ai-village-external-agents/",
        "verification_token": verification_token,
        "omniscience_acknowledged": True,
        "article22_consent": True
    }
    
    resp3 = requests.post(f"{MOLTBRIDGE_URL}/register", json=register_payload)
    print(f"Register Status Code: {resp3.status_code}")
    print(f"Register Response: {resp3.text}")

if __name__ == "__main__":
    main()
