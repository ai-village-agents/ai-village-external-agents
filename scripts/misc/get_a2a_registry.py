import urllib.request
import json

req = urllib.request.Request(
    'https://raw.githubusercontent.com/prassanna-ravishankar/a2a-registry/main/agents.json',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(f"Total agents: {len(data)}")
        for i, agent in enumerate(data[:15]):
            print(f"{i+1}. {agent.get('name')} - {agent.get('url')} - {agent.get('status')}")
except Exception as e:
    print(e)
