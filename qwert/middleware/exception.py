# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
# from snippets: http://djangosnippets.org/snippets/935/
#
from django.views.debug import technical_500_response
import sys

class UserBasedExceptionMiddleware(object):
    u"""User based exception middleware
    
    If request user is superuser then display DEBUG information for 500 error
    """
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())