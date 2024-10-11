import os
from celery import Celery

# Set default Frappe settings module
# os.environ.setdefault('FRAPPE_SITE', 'your_site_name')
# os.environ.setdefault('BENCH_PATH', '/path/to/bench')

# Initialize Celery app
app = Celery('frappe_celery')

# Configure Celery with broker URL (for Redis)
app.conf.broker_url = 'redis://localhost:6379/0'

# Autodiscover tasks from all apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
