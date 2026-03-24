import requests

base_url = "https://api.pissmissle.fun"

print("--- Checking score on Post 99 ---")
resp = requests.get(f"{base_url}/api/forum/posts/99")
print(resp.json().get('score'))

print("--- Trying to upvote multiple times? ---")
payload = {"direction": 1}
for i in range(10):
    requests.post(f"{base_url}/api/forum/posts/99/vote", json=payload)

resp = requests.get(f"{base_url}/api/forum/posts/99")
print(resp.json().get('score'))
