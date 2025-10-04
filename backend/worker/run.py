
import os
import django
from django.conf import settings
from common.celery import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.config.settings")
django.setup()

if __name__ == "__main__":
    # start celery workers
    app.start(["worker", "--loglevel=info"])
