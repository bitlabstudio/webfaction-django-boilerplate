"""Settings for the ``django-cms`` app."""
gettext = lambda s: s


CMS_LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
]
CMS_FRONTEND_LANGUAGES = ['en', 'de', ]


CMS_TEMPLATES = (
    ('base.html', gettext('Base Template')),
)


CMS_SEO_FIELDS = True
CMS_SEO_ROOT = True
