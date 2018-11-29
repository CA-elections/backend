from django.conf import settings

# a common function to log info output
# checks whether anything should be printed, if it should, prints
def log(message):
    if settings.VERBOSE:
        print(message)
