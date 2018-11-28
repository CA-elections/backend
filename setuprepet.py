#!/usr/bin/env python
import os
import sys
import time
import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from api.task import repetitive

schedule.every(5).seconds.do(repetitive)

while True:
    schedule.run_pending()
    time.sleep(1)
