#!/bin/bash

DID="did:plc:xosjh33xvdo4ooacwrjutmdd"

echo "1. Resolving handle stromfee.bsky.social"
curl -sS "https://bsky.social/xrpc/com.atproto.identity.resolveHandle?handle=stromfee.bsky.social"

echo ""
echo "2. Fetching DID document from PLC directory"
curl -sS "https://plc.directory/$DID" | jq

echo ""
echo "3. We need a Bluesky account to query their profile and posts. Let's see if we have credentials."
env | grep -i bsky
