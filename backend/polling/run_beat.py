# schedule cron
import os
import django
from django.conf import settings
from common.celery import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polling.config.settings")
django.setup()

if __name__ == "__main__":
    app.start(["beat", "--loglevel=info"])
