"""
Settings used by ``fab coverage:0``.

It verifies that at least 80% of the code is covered, before we can push

Requirements:
    - local_settings.py
    - test_settings.py
    - coverage_settings.py
"""

from coverage_settings import *  # NOQA


COVERAGE_REPORT_HTML_OUTPUT_DIR = None
