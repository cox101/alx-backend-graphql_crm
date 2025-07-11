#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import json

query = """
query {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

response = requests.post(
    "http://localhost:8000/graphql",
    json={'query': query},
    headers={'Content-Type': 'application/json'}
)

data = response.json()
with open("/tmp/order_reminders_log.txt", "a") as log:
    for order in data.get("data", {}).get("orders", []):
        log.write(f"{datetime.now()}: Order #{order['id']} - Email: {order['customer']['email']}\n")

print("Order reminders processed!")
