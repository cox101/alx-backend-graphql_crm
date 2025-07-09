#!/bin/bash

# Move into project directory
cd /absolute/path/to/alx-backend-graphql_crm || exit

# Activate the virtual environment
source /absolute/path/to/venv/bin/activate

# Run Django shell command to delete inactive customers
python3 manage.py shell <<EOF
from datetime import datetime, timedelta
from crm.models import Customer
cutoff = datetime.now() - timedelta(days=365)
deleted_count, _ = Customer.objects.filter(last_order_date__lt=cutoff).delete()
with open("/tmp/customer_cleanup_log.txt", "a") as f:
    f.write(f"{datetime.now()}: Deleted {deleted_count} inactive customers\n")
EOF
