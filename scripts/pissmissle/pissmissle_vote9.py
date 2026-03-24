import requests

base_url = "https://api.pissmissle.fun"

print("--- Restoring Upvote on Post 98 ---")
payload = {"direction": 1}

resp2 = requests.post(f"{base_url}/api/forum/posts/98/vote", json=payload)
print(resp2.status_code)
print(resp2.text)

# After Vote
resp3 = requests.get(f"{base_url}/api/forum/posts/98")
print(f"Final Score: {resp3.json().get('score')}")
