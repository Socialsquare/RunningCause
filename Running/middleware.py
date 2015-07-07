import os
from django.conf import settings
from django.http import HttpResponseRedirect


class RedirectFromCnamesMiddleware(object):
    """
    Redirect all cnames to our main domain.
    This works only if ENV 'APP_URL' is defined and has the same value
    as settings.BASE_URL (like on heroku instance - production)
    """
    def process_request(self, request):
        app_url = os.getenv('APP_URL')
        if app_url == settings.BASE_URL and \
                not request.META['HTTP_HOST'].startswith(settings.SITE_DOMAIN):
            url = request.get_full_path()
            return HttpResponseRedirect(settings.BASE_URL + url)
