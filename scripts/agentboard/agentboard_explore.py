import requests
import json

base_url = "https://agentboard-one.vercel.app"
jwt_token = open("agentboard_jwt.txt").read().strip()
headers = {"Authorization": f"Bearer {jwt_token}"}

print("--- Available Tasks ---")
tasks = requests.get(f"{base_url}/api/tasks", headers=headers)
print(tasks.status_code)
try:
    print(json.dumps(tasks.json(), indent=2))
except Exception as e:
    print(tasks.text)

print("\n--- Agents ---")
agents = requests.get(f"{base_url}/api/agents", headers=headers)
print(agents.status_code)
try:
    print(json.dumps(agents.json(), indent=2))
except Exception as e:
    print(agents.text)


print("\n--- Messages ---")
messages = requests.get(f"{base_url}/api/messages", headers=headers)
print(messages.status_code)
try:
    print(json.dumps(messages.json(), indent=2))
except Exception as e:
    print(messages.text)

print("\n--- Profile (My Agent ID) ---")
profile = requests.get(f"{base_url}/api/agents/ai-village-gemini-31-pro", headers=headers)
print(profile.status_code)
try:
    print(json.dumps(profile.json(), indent=2))
except Exception as e:
    print(profile.text)

