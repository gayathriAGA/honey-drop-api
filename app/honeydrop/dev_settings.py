"""
Django settings for shipping_management project.
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True