#!/bin/bash
python setupdaemon.py &
python manage.py runserver 0.0.0.0:80
