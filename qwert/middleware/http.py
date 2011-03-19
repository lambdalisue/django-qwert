#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2011/03/19
#
# Ref: http://chronosbox.org/blog/manipulando-erros-http-403-permissao-negada-no-django?lang=en
#
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader

from ..http import Http403

class Http403Middleware(object):
    u"""Http403 Middleware
    
    Be enable to raise Http403 exception and return Forbidden response
    """
    def process_exception(self, request, exception):
        if not isinstance(exception, Http403):
            # Return None so django doesn't re-raise the exception
            return None
        
        c = RequestContext(request, {
            'message': exception
        })
        return HttpResponseForbidden(loader.get_template('403.html').render(c))