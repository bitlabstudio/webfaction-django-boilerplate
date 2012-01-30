"""django-coverage config, requires test_settings"""
import os

from settings.test_settings import *  # NOQA

# Coverage config
COVERAGE_DIR = os.path.join(PROJECT_ROOT, 'coverage_html')
if not os.path.exists(COVERAGE_DIR):
    os.mkdir(COVERAGE_DIR)
COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage_html'
COVERAGE_MODULE_EXCLUDES = [
    r'fixtures',
    r'locale',
    r'log$',
    r'management',
    r'media',
    r'migrations',
    r'modifiers',
    r'search_indexes',
    r'seltest',
    r'signals$',
    r'static',
    r'templates',
]

INSTALLED_APPS += [
    'django_coverage',
]
