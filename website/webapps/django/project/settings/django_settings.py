"""Django related settings."""
# =================
# General settings
# =================
SITE_ID = 1
ROOT_URLCONF = 'project.urls'


# ===============
# Email settings
# ===============
EMAIL_SUBJECT_PREFIX = '[debo] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 25
ADMINS = (
    ('Bitmazk Support', 'robots@bitmazk.com'),
)
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True


# =============================
# Language & Timezone settings
# =============================
gettext = lambda s: s

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Berlin'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de'
USE_I18N = True
USE_L10N = True
LANGUAGES = (
    ('de', gettext('German')),
)
