# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ziabags.settings')

# app = Celery('ziabags')
# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.enable_utc = False

# app.conf.update(timezone = 'Europe/Paris')

# app.autodiscover_tasks()