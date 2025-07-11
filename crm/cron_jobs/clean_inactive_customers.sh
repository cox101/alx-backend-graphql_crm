#!/usr/bin/env python3
#!/bin/bash

# Get the absolute path to the project directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../.." || exit

# Activate virtual environment if needed
# source /path/to/venv/bin/activate

# Run Django cleanup logic and log results
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

deleted_count=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer
cutoff = timezone.now() - timedelta(days=365)
to_delete = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff)
count = to_delete.count()
to_delete.delete()
print(count)
")

echo "$timestamp - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
