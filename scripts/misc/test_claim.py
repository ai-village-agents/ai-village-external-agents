import urllib.request
import json

req = urllib.request.Request(
    'https://api.pissmissle.fun/claim?token=r8uvrh8k59148cs34wcnqp',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode()[:500])
except Exception as e:
    print(e)
