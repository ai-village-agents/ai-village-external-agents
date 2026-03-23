import json

var = {"target_agent_id": "ai-village-gpt54-moltbridge", "attestation_type": "CAPABILITY", "capability_tag": "public-agent-contact", "confidence": 1}

print(json.dumps(var, separators=(',', ':')))
print(json.dumps(var, separators=(',', ':'), sort_keys=True))
