#!/usr/bin/env python
import os
import sys
import time
import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from api.daemon import runtasks

schedule.every(5).seconds.do(runtasks)

while True:
    schedule.run_pending()
    time.sleep(1)
