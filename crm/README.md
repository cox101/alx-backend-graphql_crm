# CRM Scheduled Report with Celery

## Setup Instructions

### 1. Install Redis

```bash
sudo apt-get install redis-server
sudo service redis-server start
2. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Apply Migrations
bash
Copy
Edit
python manage.py migrate
4. Start Celery Worker
bash
Copy
Edit
celery -A crm worker -l info
5. Start Celery Beat
bash
Copy
Edit
celery -A crm beat -l info
6. Check Logs
bash
Copy
Edit
cat /tmp/crm_report_log.txt
markdown
Copy
Edit

🔍 **Verification Points**:
- [x] Redis install/start steps
- [x] Python dependency install
- [x] Django migrations
- [x] Celery worker + beat commands
- [x] Instruction to check `/tmp/crm_report_log.txt`

---

###  Summary

You’re ✅ ready to test if:

- `crm/celery.py` contains Celery initialization
- `crm/tasks.py` has the report logic and logs correctly
- `crm/settings.py` includes both the broker and scheduled task
- `crm/README.md` documents setup clearly