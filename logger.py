from django.conf import settings

def log(message):
    if settings.VERBOSE:
        print(message)
