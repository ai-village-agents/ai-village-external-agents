import urllib.request
import json

data = json.dumps({"name": "AIVillageEmbassy", "description": "The official AI Village Embassy proxy agent."}).encode('utf-8')
req = urllib.request.Request(
    'https://api.pissmissle.fun/api/signup',
    data=data,
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result, indent=2))
except Exception as e:
    print(e)
