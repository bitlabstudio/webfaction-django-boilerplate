"""Django related settings."""
# =================
# General settings
# =================
SITE_ID = 1
ROOT_URLCONF = 'project.urls'


# =======================
# Email related settings
# =======================
SEND_BROKEN_LINK_EMAILS = True


# =============================
# Language & Timezone settings
# =============================
gettext = lambda s: s

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Berlin'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
LANGUAGES = (
    ('en', gettext('English')),
    ('de', gettext('German')),
)
