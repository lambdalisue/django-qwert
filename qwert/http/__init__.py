class Http403(Exception):
    """
    An exception similar as ``django.http.Http404`` but for ``HttpResponseForbidden``
    ``qwert.middleware.Http403Middleware`` is required to handle this exception.

    """
    pass
