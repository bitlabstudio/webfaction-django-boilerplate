"""Media and staticfiles related settings."""
import os

from settings.base_settings import PROJECT_ROOT


# Make sure to set MEDIA_ROOT and STATIC_ROOT in your local_settings.py
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
