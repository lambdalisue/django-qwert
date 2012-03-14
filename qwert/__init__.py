# vim: set fileencoding=utf-8 :
version = (0, 2, 0)
__version__ = '.'.join(map(str, version))

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
