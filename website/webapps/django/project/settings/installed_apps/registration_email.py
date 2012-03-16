"""Settings for the ``django-registration-email`` app."""


ACCOUNT_ACTIVATION_DAYS = 7
AUTHENTICATION_BACKENDS = (
    'registration_email.auth.EmailBackend',
)
LOGIN_REDIRECT_URL = '/'
