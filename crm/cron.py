#!/usr/bin/env python3
import datetime
import requests

def log_crm_heartbeat():
    """Logs heartbeat message and optionally checks GraphQL hello endpoint."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append message to log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    # Optional: verify the hello field from GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            headers={"Content-Type": "application/json"},
            timeout=3,
        )
        if response.status_code == 200:
            result = response.json()
            hello_value = result.get("data", {}).get("hello", "")
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"{timestamp} GraphQL hello: {hello_value}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL hello check failed: {e}\n")