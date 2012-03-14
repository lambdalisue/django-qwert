django-qwert is a trivia snippet collection of Django which used in 
`Kawaz <http://www.kawaz.org>`_

Install
==============
::

    pip install django-qwert

Features
================

1.  Http403 exception

    Like ``Http404`` exception. You can raise ``Http403`` exception and
    ``HttpResponseForbidden`` will be responsed

2.  User based exception

    Super user can see Django technical exception page even when
    ``DEBUG=False``

3.  Global request

    Developpers can access ``request`` instance duaring request process
    with thread local mechanisms

4.  ``with_request`` decorator

    To enable handling ``request`` instance in form, convert form class and 
    classbased generic view class. It is useful to determine the author of
    the object in method of form.

5.  Useful templatetags and some extra builtin templatetags

    +   expr (extra builtin)

        calculate python expression in template

    +   evaluate

        evaluate django template in string

    +   truncateletters (extra builtin)
    
        like ``truncatewords``, this truncate letters. Useful to use the
        language which does not have space for delimiter (like Japanese,
        Chinese ...etc)

    +   markdown

        enhanced markdown filter which can care about the markdown extensions.
        ``markdown`` is required to use this templatetag.

    +   urlize_html

        ``urlize`` filter for HTML string. ``BeautifulSoup`` is required to
        use this templatetag

6.  Enhanced override_settings

    Similar with Django 1.4 ``override_settings`` but it will recall
    ``syncdb`` command when new app is appended to ``INSTALLED_APPS``.
    And ``with_apps`` and ``without_apps`` decorator/context manager is 
    added.

7.  Automatically test user is created in ``syncdb`` command

Settings
================

``AUTO_CREATE_TESTUSER``
    To disable automatically creating test user in ``syncdb`` command, set
    ``False`` to this setting. Default: ``True``

``TESTUSER_USERNAME``
    An username of test user. Default: ``'admin'``

``TESTUSER_EMAIL``
    An email address of test user. Default: ``"%s@test.com" %
    TESTUSER_USERNAME``

``TESTUSER_PASSWORD``
    A password of test user. Default: ``'password'``

``ENABLE_EXTRA_BUILTINS``
    To disable adding extra templatetags to buitlin, set ``False``. 

