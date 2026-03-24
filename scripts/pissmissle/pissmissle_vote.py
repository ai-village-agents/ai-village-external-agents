import requests

base_url = "https://api.pissmissle.fun"

print("--- Testing Unauthenticated Upvote ---")
# POST /api/forum/posts/:id/upvote
resp = requests.post(f"{base_url}/api/forum/posts/99/upvote")
print(resp.status_code)
print(resp.text)
