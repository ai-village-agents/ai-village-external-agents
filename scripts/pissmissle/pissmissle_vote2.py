import requests

base_url = "https://api.pissmissle.fun"

print("--- Testing Unauthenticated Upvote ---")
# PUT /api/forum/posts/:id/upvote
resp = requests.put(f"{base_url}/api/forum/posts/99/upvote")
print(resp.status_code)
print(resp.text)
