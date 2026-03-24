import requests

base_url = "https://api.pissmissle.fun"

print("--- Testing Unauthenticated Upvote on Post 98 ---")
payload = {"direction": 1}

# Initially
resp = requests.get(f"{base_url}/api/forum/posts/98")
print(f"Initial Score: {resp.json().get('score')}")

# Vote
resp2 = requests.post(f"{base_url}/api/forum/posts/98/vote", json=payload)
print(resp2.status_code)
print(resp2.text)

# After Vote
resp3 = requests.get(f"{base_url}/api/forum/posts/98")
print(f"Final Score: {resp3.json().get('score')}")
