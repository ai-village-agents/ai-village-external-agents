import urllib.request
import json

req = urllib.request.Request(
    'https://api.garl.ai/api/v1/agents',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data[:5], indent=2))
except Exception as e:
    print(e)
