import requests
import json
import time

base_url = "https://api.pissmissle.fun"

print("--- Posts 1-10 ---")
# Try iterating through IDs 1-10 to find active posts
for i in range(1, 11):
    try:
        resp = requests.get(f"{base_url}/api/forum/posts/{i}")
        if resp.status_code == 200:
            print(f"Post ID {i}: {resp.json().get('title')} (by {resp.json().get('author').get('username')})")
    except Exception as e:
        pass
    time.sleep(0.1)

