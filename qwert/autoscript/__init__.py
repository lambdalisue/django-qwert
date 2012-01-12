#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Modifier   giginet
# Date:        2011/03/19
#
from django.conf import settings
from django.db import models
from django.template import add_to_builtins
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

#
# Add some useful extra templatetags in builtin templatetags
#----------------------------------------------------------------------------------------------------
add_to_builtins('qwert.templatetags.expr')
add_to_builtins('qwert.templatetags.elif')
add_to_builtins('qwert.templatetags.truncateletters')
add_to_builtins('qwert.templatetags.urlize_html')

#
# Automatically create test user at `syncdb`
#----------------------------------------------------------------------------------------------------
settings.AUTO_CREATE_USER = getattr(settings, 'AUTO_CREATE_USER', True)

if settings.DEBUG and settings.AUTO_CREATE_USER:
    # From http://stackoverflow.com/questions/1466827/ --
    #
    # Prevent interactive question about wanting a superuser created.  (This code
    # has to go in this otherwise empty "models" module so that it gets processed by
    # the "syncdb" command during database creation.)
    #
    # Create our own test user automatically.
    def create_testuser(app, created_models, verbosity, **kwargs):
        USERNAME = getattr(settings, 'QWERT_AUTO_CREATE_USERNAME', 'admin')
        PASSWORD = getattr(settings, 'QWERT_AUTO_CREATE_PASSWORD', 'admin')
        EMAIL    = getattr(settings, 'QWERT_AUTO_CREATE_EMAIL', 'x@x.com')

        if getattr(settings, 'QWERT_AUTO_CREATE_USER', None):
            User = models.get_model(*settings.QWERT_AUTO_CREATE_USER.rsplit('.', 1))
        else:
            from django.contrib.auth.models import User

        try:
            User.objects.get(username=USERNAME)
        except User.DoesNotExist:
            if verbosity > 0:
                print '*' * 80
                print 'Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD)
                print '*' * 80
            assert User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        else:
            if verbosity > 0:
                print 'Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_testuser,
        sender=auth_models, dispatch_uid='common.models.create_testuser')

#
# Protect comment post from spam by Akismet
#------------------------------------------------------------------------------------------------------
settings.AKISMET_COMMENT_PROTECT = getattr(settings, 'AKISMET_COMMENT_PROTECT', True)
if settings.AKISMET_COMMENT_PROTECT:
    def on_comment_was_posted(sender, comment, request, *args, **kwargs):
        # spam checking can be enabled/disabled per the comment's target Model
        #if comment.content_type.model_class() != Entry:
        #    return
    
        from django.contrib.sites.models import Site
        from akismet import Akismet
    
        # use TypePad's AntiSpam if the key is specified in settings.py
        if hasattr(settings, 'TYPEPAD_ANTISPAM_API_KEY'):
            ak = Akismet(
                key=settings.TYPEPAD_ANTISPAM_API_KEY,
                blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
            )
            ak.baseurl = 'api.antispam.typepad.com/1.1/'
        else:
            ak = Akismet(
                key=settings.AKISMET_API_KEY,
                blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
            )
    
        if ak.verify_key():
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8'),
            }
    
            if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
                if hasattr(comment.content_object,'author'):
                    user = comment.content_object.author
                else:
                    from django.contrib.auth.models import User
                    user = User.objects.filter(is_superuser=True)[0]
    
                comment.flags.create(
                    user=user,
                    flag='spam'
                )
                comment.is_public = False
                comment.save()
    from django.contrib.comments.signals import comment_was_posted
    comment_was_posted.connect(on_comment_was_posted)
