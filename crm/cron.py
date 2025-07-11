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

def update_low_stock():
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                updatedProducts
            }
        }
    """)
    try:
        result = client.execute(mutation)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} Updated products: {result['updateLowStockProducts']['updatedProducts']}\n")
    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} Error during update: {str(e)}\n")   