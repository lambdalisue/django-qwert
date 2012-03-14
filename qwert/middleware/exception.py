# vim: set fileencoding=utf-8 :
# from snippets: http://djangosnippets.org/snippets/935/
import sys
from django.views.debug import technical_500_response


class UserBasedExceptionMiddleware(object):
    """User based exception middleware
    
    If request user is superuser then display DEBUG information for 500 error
    """
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
        return None
