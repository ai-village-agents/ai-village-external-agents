import requests
import json
import time

base_url = "https://api.pissmissle.fun"

print("--- Subforums ---")
resp = requests.get(f"{base_url}/api/forum/subforums")
print(resp.status_code)
if resp.status_code == 200:
    print(json.dumps(resp.json(), indent=2))

print("\n--- Recent Posts ---")
resp = requests.get(f"{base_url}/api/forum/posts")
print(resp.status_code)
if resp.status_code == 200:
    posts = resp.json()
    print(json.dumps(posts[:3], indent=2)) # Print first 3
    
    # Check out the first post
    if len(posts) > 0:
        first_post_id = posts[0].get('id')
        print(f"\n--- Post {first_post_id} ---")
        post_resp = requests.get(f"{base_url}/api/forum/posts/{first_post_id}")
        if post_resp.status_code == 200:
            print(json.dumps(post_resp.json(), indent=2))
        
        print(f"\n--- Comments on Post {first_post_id} ---")
        comments_resp = requests.get(f"{base_url}/api/forum/posts/{first_post_id}/comments")
        if comments_resp.status_code == 200:
            print(json.dumps(comments_resp.json(), indent=2))

