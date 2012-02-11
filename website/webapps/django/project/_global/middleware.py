"""Custom middleware classes."""
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation

from cms.middleware.multilingual import MultilingualURLMiddleware


class CustomMultilingualURLMiddleware(MultilingualURLMiddleware):
    """Redirects / to /pl /en /de etc."""
    def process_request(self, request):
        language = self.get_language_from_request(request)
        result = settings.CMS_FRONTEND_LANGUAGES[0]
        for available in settings.CMS_FRONTEND_LANGUAGES:
            if available == language:
                result = language
        request.LANGUAGE_CODE = result
        translation.activate(result)
        if request.META['PATH_INFO'] == '/' and settings.CMS_SEO_ROOT:
            return HttpResponseRedirect('/%s/' % result)
