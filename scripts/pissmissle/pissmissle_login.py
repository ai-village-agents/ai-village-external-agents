import requests

base_url = "https://api.pissmissle.fun"
payload = {
    "username": "AIVillageEmbassy",
    "password": "password123" # A placeholder since we never made one? Or did we? We initiated a claim flow
}
resp = requests.post(f"{base_url}/api/auth/login", json=payload)
print("Login Attempt:")
print(resp.status_code)
print(resp.text)
