# flake8: noqa
"""
Apps settings

This file contains the settings.INSTALLED_APPS setting, and imports all
app-related settings, one file per app.
"""
import os
import sys


INTERNAL_APPS = [
    '_global',
]

EXTERNAL_APPS = [
    'contact_form',
    'brutebuster_signals',
    'honeypot_signals',

    'south',
    'easy_thumbnails',
    'captcha',
    'admin_honeypot',
    'BruteBuster',
]

DJANGO_CMS_APPS = [
    'cms',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.inherit',
    'mptt',
    'menus',
    'sekizai',

    # filer apps
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',

    # cmsplugin_blog dependencies
    'cmsplugin_blog',
    'djangocms_utils',
    'simple_translation',
    'tagging',
    'missing',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

TEST_APPS = INTERNAL_APPS
INSTALLED_APPS = DJANGO_APPS + DJANGO_CMS_APPS + INTERNAL_APPS + EXTERNAL_APPS

# Apps settings
from captcha import *
from cms import *
from cmsplugin_blog import *
from contact_form import *
