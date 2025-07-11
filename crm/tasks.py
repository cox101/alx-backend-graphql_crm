
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        allCustomers { totalCount }
        allOrders { totalCount }
        orders { totalamount }
    }
    """)

    try:
        result = client.execute(query)
        customer_count = result['allCustomers']['totalCount']
        order_count = result['allOrders']['totalCount']
        total_revenue = sum([float(order['totalamount']) for order in result['orders']])

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{now} - Report: {customer_count} customers, {order_count} orders, {total_revenue} revenue\n")
    except Exception as e:
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{datetime.now()} - ERROR: {str(e)}\n")
