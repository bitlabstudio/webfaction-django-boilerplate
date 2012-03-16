from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False and settings.SANDBOX is True:
    urlpatterns += patterns('',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin-XXXX/', include(admin.site.urls)),
    url(r'^admin-.+/', include('admin_honeypot.urls')),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^accounts/', include('registration_email.backends.default.urls')),
    url(r'^', include('cms.urls')),
)
