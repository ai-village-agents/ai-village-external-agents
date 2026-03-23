import requests
import hashlib
import json
import base64
import sys
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

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
    if len(sys.argv) != 5:
        print("Usage: complete_registration.py <challenge_id> <nonce> <difficulty> <cognitive_answer>")
        sys.exit(1)
        
    challenge_id = sys.argv[1]
    nonce = sys.argv[2]
    difficulty = int(sys.argv[3])
    cog_solution = sys.argv[4]

    print("\n--- Step 2 & 3: Solve Challenges ---")
    pow_solution = solve_pow(nonce, difficulty)

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
        
    verification_token = verify_data.get('token')
    if not verification_token:
         print("Failed to get verification token.")
         return

    print(f"Verification successful! Token: {verification_token}")

    print("\n--- Step 5: Generate Ed25519 Keys ---")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    raw_pubkey_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    b64url_pubkey = base64.urlsafe_b64encode(raw_pubkey_bytes).decode('utf-8').rstrip('=')
    
    pem_priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("moltbridge_priv.pem", "wb") as f:
        f.write(pem_priv)
    print("Saved private key to moltbridge_priv.pem")
    print(f"Base64URL Raw PubKey: {b64url_pubkey}")

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
