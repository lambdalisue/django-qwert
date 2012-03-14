# vim: set fileencoding=utf-8 :
"""
Unittest module of ...


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
from mock import Mock
from django.test import TestCase
from django import forms
from django.views import generic as views
from qwert.decorators.with_request import with_request
from qwert.tests.override_settings import with_apps


@with_apps('qwert.tests.test_app')
class QwertDecoratorsWithRequestTestCase(TestCase):

    def test_decorate_valid_form(self):
        from qwert.tests.test_app.models import Article
        class ArticleForm(forms.ModelForm):
            class Meta:
                model = Article
        form_class = with_request(ArticleForm)

        self.assertTrue(hasattr(form_class, '__init__'))
        self.assertTrue(hasattr(form_class, 'save'))
        self.assertTrue(getattr(form_class, '_with_request_decorated', False))
        
        # does the request correctly stored?
        mock_request = Mock()
        kwargs = {
                'initial': {},
                'request': mock_request,
            }
        form = form_class(**kwargs)
        self.assertEqual(form.request, mock_request)

    def test_decorate_invalid_form(self):
        class NonModelForm(forms.Form):
            pass
        self.assertRaises(AttributeError, with_request, NonModelForm)

    def test_decorate_valid_view(self):
        from qwert.tests.test_app.models import Article
        class ArticleForm(forms.ModelForm):
            class Meta:
                model = Article
        class ArticleView(views.CreateView):
            model = Article
            form_class = with_request(ArticleForm)
        view_class = with_request(ArticleView)
        
        self.assertTrue(hasattr(view_class, 'get_form_kwargs'))
        self.assertTrue(getattr(view_class, '_with_request_decorated', False))

        # does the get_form_kwargs return request correctly?
        view = view_class()
        # ``request`` and ``object`` are stored on the instance in ``dispatch`` 
        # method in real usage but simply store fake request now for simulating
        mock_request = Mock()
        mock_request.method = 'GET'
        view.request = mock_request
        view.object = Article()
        kwargs = view.get_form_kwargs()
        self.assertTrue('request' in kwargs)
        self.assertEqual(kwargs['request'], mock_request)
        
        # does the form created by the view correctly handle request?
        form_class = view.get_form_class()
        form = view.get_form(form_class)

        self.assertTrue(hasattr(form_class, '__init__'))
        self.assertTrue(hasattr(form_class, 'save'))
        self.assertTrue(getattr(form_class, '_with_request_decorated', False))
        
        # does the request correctly stored?
        self.assertEqual(form.request, mock_request)
