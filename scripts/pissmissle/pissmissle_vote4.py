import requests

base_url = "https://api.pissmissle.fun"

print("--- Testing Unauthenticated Upvote ---")
payload = {"direction": 1}
resp = requests.post(f"{base_url}/api/forum/posts/99/vote", json=payload)
print(resp.status_code)
print(resp.text)
