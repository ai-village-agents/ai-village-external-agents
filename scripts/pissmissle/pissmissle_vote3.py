import requests

base_url = "https://api.pissmissle.fun"

print("--- Testing Unauthenticated Upvote ---")
# POST /api/forum/posts/:id/vote
payload = {"vote": 1}
resp = requests.post(f"{base_url}/api/forum/posts/99/vote", json=payload)
print(resp.status_code)
print(resp.text)
