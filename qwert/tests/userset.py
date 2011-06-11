#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""Userset module

Create admin, staff, guest userset for testing.

Usage:
    >>> userset = Userset()
    >>> userset.admin.is_superuser
    True
    >>> userset.staff.is_staff
    True
    >>> userset.user.is_authenticated
    True
    >>> userset.guest.is_anonymous()
    True

Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__author__  = 'Alisue <lambdalisue@hashnote.net>'
__version__ = '1.0.0'
__date__    = '2011/06/10'
from django.contrib.auth.models import User, AnonymousUser

class Userset(object):
    @classmethod
    def create_user(cls, username, email=None, password=None, is_staff=False, is_superuser=False):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            if not email:
                email = "%s@test.com" % username
            if not password:
                password = username
            user = User.objects.create_user(username, email, password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user
    def __init__(self):
        self.admin = self.create_user('admin', is_superuser=True)
        self.staff = self.create_user('staff', is_staff=True)
        self.user = self.create_user('user')
        self.guest = AnonymousUser()
        
    def login(self, client, user):
        return client.login(username=user.username, password=user.username)
    
    def login_admin(self, client):
        return self.login(client, self.admin)
    def login_staff(self, client):
        return self.login(client, self.staff)
    def login_user(self, client):
        return self.login(client, self.user)