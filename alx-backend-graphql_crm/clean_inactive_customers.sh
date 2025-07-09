#!/bin/bash
cd /absolute/path/to/your/project || exit
source /absolute/path/to/your/venv/bin/activate

python3 manage.py shell << END
from datetime import datetime, timedelta
from crm.models import Customer
cutoff = datetime.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=cutoff).delete()
with open("/tmp/customer_cleanup_log.txt", "a") as log:
    log.write(f"{datetime.now()}: Deleted {deleted} inactive customers.\n")
END
# Ensure the script is executable
chmod +x /absolute/path/to/your/project/clean_inactive_customers.sh
