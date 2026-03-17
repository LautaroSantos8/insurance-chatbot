from config.settings import *
from config.paths import STORAGE_DIR
import os

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f"{os.path.join(STORAGE_DIR, 'django_db.sqlite3')}",
    }
}
