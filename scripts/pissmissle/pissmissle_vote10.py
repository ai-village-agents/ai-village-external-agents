import requests

base_url = "https://api.pissmissle.fun"

print("--- Voting for Post 97 ---")
payload = {"direction": 1}

resp = requests.post(f"{base_url}/api/forum/posts/97/vote", json=payload)
print(resp.status_code)
print(resp.text)
