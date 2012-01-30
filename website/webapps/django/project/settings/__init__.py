# flake8: noqa
"""
Django settings split into different files for better maintenance and
visibility.
"""
from settings.base_settings import *
from settings.installed_apps import *
from settings.staticfiles_settings import *
from settings.middleware_settings import *
from settings.django_settings import *
from settings.templates_settings import *
from settings.local.local_settings import *
