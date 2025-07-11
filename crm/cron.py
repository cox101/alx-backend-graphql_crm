#!/usr/bin/env python3
import datetime
import requests

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_entry = f"{timestamp} CRM is alive\n"

    # Log to file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_entry)

    # Optional GraphQL health check
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql('query { hello }')
        response = client.execute(query)
        print("GraphQL Hello Response:", response)
    except Exception as e:
        print("GraphQL Health Check Failed:", e)