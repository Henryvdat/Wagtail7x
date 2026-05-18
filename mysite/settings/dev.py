from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Suppress Django template DEBUG logging to avoid Python 3.14 logging recursion bug.
# Django logs a debug message for every failed template variable lookup; in Python 3.14
# this triggers infinite recursion in logging/__init__.py.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "django.template": {
            "level": "INFO",
        },
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-buy^^f37tb$xp1$vzhsxh42xl5$5_b9-^h5xodvv-gg%2hayev"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
