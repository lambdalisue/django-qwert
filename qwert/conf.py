# vim: set fileencoding=utf-8 :
"""
Configure


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
from __future__ import with_statement
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def checkconf(name, msg):
    """check django.conf.settings is proprely configured"""
    if not hasattr(settings, name):
        raise ImproperlyConfigured(msg)

def setconf(name, default_value):
    """set default value to django.conf.settings"""
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)


# qwert.management.create_testuser
setconf('AUTO_CREATE_TESTUSER', settings.DEBUG)
setconf('TESTUSER_USERNAME', 'admin')
setconf('TESTUSER_EMAIL', '%s@test.com' % settings.TESTUSER_USERNAME)
setconf('TESTUSER_PASSWORD', 'password')

# qwert.management.extra_builtins
setconf('ENABLE_EXTRA_BUILTINS', True)
