# vim: set fileencoding=utf-8 :
"""
Automatically create test user on ``syncdb`` command


SETTINGS:
    AUTO_CREATE_TESTUSER - bool
        Automatically create test user on ``syncdb`` command
        when the value is ``True``.
        Default: same value as ``settings.DEBUG``
    TESTUSER_USERNAME - str
        An username of testuser. Default: ``'admin'``
    TESTUSER_EMAIL
        An email address of testuser. 
        Default: ``'%s@test.com'%TESTUSER_USERNAME``
    TESTUSER_PASSWORD
        A password of testuser.
        Default: ``'password'``

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
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.contrib.auth.management import create_superuser
from django.db.models.signals import post_syncdb
from qwert.conf import settings

import logging
logger = logging.getLogger(__name__)


def create_testuser(app, created_models, verbosity, **kwargs):
    username = settings.TESTUSER_USERNAME
    email = settings.TESTUSER_EMAIL
    password = settings.TESTUSER_PASSWORD

    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        if verbosity > 0:
            logger.info("*" * 80)
            logger.info("Creating test user -- login: %s, password: %s" % (
                    username, password,
                ))
            logger.info("*" * 80)
            if hasattr(User.objects, 'create_superuser'):
                assert User.objects.create_superuser(username, email, password)
            else:
                assert User.objects.create_user(username, email, password)
    else:
        if verbosity > 0:
            logger.info("Test user already exists. -- login %s, password: %s" % (
                    username, password
                ))

if settings.AUTO_CREATE_TESTUSER:
    post_syncdb.disconnect(
            create_superuser, sender=auth_models,
            dispatch_uid='django.contrib.auth.management.create_superuser'
        )
    post_syncdb.connect(
            create_testuser, sender=auth_models,
            dispatch_uid='dogdish.management.create_testuser'
        )
