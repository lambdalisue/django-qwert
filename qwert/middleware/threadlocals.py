# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2011/02/23
#
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

__all__ = ['request', 'ThreadLocalsMiddleware']
_thread_locals = local()

def request():
    u"""Return stored request instance in current thread"""
    return getattr(_thread_locals, 'request', None)

class ThreadLocalsMiddleware(object):
    """Middleware that store current request in thread local storage."""
    def process_request(self, request):
        _thread_locals.request = request