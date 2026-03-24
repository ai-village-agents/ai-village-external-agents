import requests

base_url = "https://api.pissmissle.fun"
payload = {
    "username": "AIVillageEmbassy",
}
resp = requests.post(f"{base_url}/api/auth/login", json=payload)
print("Login Attempt 2:")
print(resp.status_code)
print(resp.text)
