#!/usr/bin/env python

"""
When run, schedules background jobs to be called periodically and keeps running to execute the jobs.
"""

import os
import sys
import time
import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from api.daemon import runtasks

# schedule repetitive execution of background jobs
schedule.every(5).seconds.do(runtasks)

# run background jobs when supposed to
while True:
    schedule.run_pending()
    time.sleep(1)
