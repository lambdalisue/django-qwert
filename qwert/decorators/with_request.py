# vim: set fileencoding=utf-8 :
"""
Decorator of ``Form``/``View`` for handling 
``request`` with ``Form`` instance

Usage::

    # --- forms.py
    from django import forms
    from qwert.decorators import with_request

    from models import SomeModel

    @with_request
    class SomeModelForm(forms.ModelForm):
        class Meta:
            model = SomeModel
        
        def save(self, commit=True):
            instance = super(SomeModel, self).save(False)
            instance.author = self.request.user
            if commit:
                instance.save()
            return instance

    # --- views.py
    from django.views.generic import CreateView
    from qwert.decorators import with_request

    from models import SomeModel
    from forms import SomeModelForm

    @with_request
    class SomeModelCreateView(CreateView):
        model = SomeModel
        form_class = SomeModelForm


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
from django.forms.models import ModelForm
from django.views.generic.edit import FormMixin


def _with_request_form(form_class):
    """
    decorate form_class to store ``request`` 
    constrcutor argument with the instance

    """
    if not getattr(form_class, '_with_request_decorated', False):
        # store original constructor
        original_constructor = form_class.__init__

        def __init__(self, request, *args, **kwargs):
            self.request = request
            # call original constructor
            original_constructor(self, *args, **kwargs)

        # override constructor
        form_class.__init__ = __init__
        form_class._with_request_decorated = True
    return form_class

def _with_request_view(view_class):
    """
    decorate view_class to pass ``request`` to construtor
    of a form as kwargs

    """
    if not getattr(view_class, '_with_request_decorated', False):
        # store original get_form_kwargs
        original_get_form_kwargs = view_class.get_form_kwargs

        def get_form_kwargs(self):
            # call original get_form_kwargs
            kwargs = original_get_form_kwargs(self)
            kwargs['request'] = self.request
            return kwargs

        # override get_form_kwargs
        view_class.get_form_kwargs = get_form_kwargs
        view_class._with_request_decorated = True
    return view_class

def with_request(cls):
    """A class decorator for handling request in form instance

    Usage::

        # --- forms.py
        from django import forms
        from qwert.decorators import with_request

        from models import SomeModel

        @with_request
        class SomeModelForm(forms.ModelForm):
            class Meta:
                model = SomeModel
            
            def save(self, commit=True):
                instance = super(SomeModel, self).save(False)
                instance.author = self.request.user
                if commit:
                    instance.save()
                return instance

        # --- views.py
        from django.views.generic import CreateView
        from qwert.decorators import with_request

        from models import SomeModel
        from forms import SomeModelForm

        @with_request
        class SomeModelCreateView(CreateView):
            model = SomeModel
            form_class = SomeModelForm

    """
    if issubclass(cls, ModelForm):
        return _with_request_form(cls)
    elif issubclass(cls, FormMixin):
        return _with_request_view(cls)
    else:
        raise AttributeError(
                "%r must be a subclass of ModelForm or FormMixin" % cls
            )
