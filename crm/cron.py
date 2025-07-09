#!/usr/bin/env python3
from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    try:
        res = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        status = res.status_code
        message = res.json().get("data", {}).get("hello", "No response")
    except Exception as e:
        status = "fail"
        message = str(e)

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(f"{timestamp} CRM is alive - Status: {status} - Message: {message}\n")
