# vim: set fileencoding=utf-8 :
"""
evaluate context variable as django template.


Usage:

    {% evaluate object.textfield %}
    {% evaluate object.textfield based 'base.html' %}

Example:

    `flatpages/default.html`
        {% load evaluate_tag %}
        {% evaluate flatpage.content based 'base.html' %}
        
    flatpage content on db

        {% block head %}
        <title>{{ flatpage.title }}</title>
        {% endblock %}
        
        {% block content %}
        <h1>This is a test</h1>
        {% endblock %}


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
from django.template import Node
from django.template import Library
from django.template import Variable
from django.template import Template
from django.template import VariableDoesNotExist
from django.template import TemplateSyntaxError

register = Library()


class EvaluateNode(Node):
    def __init__(self, template, based=None):
        self.template = template
        self.based = based

    def render(self, context):
        try:
            content = self.template.resolve(context)
            if self.based:
                based = self.based.resolve(context)
                content = u"""{%% extends "%s" %%}\n%s""" % (based, content)
            t = Template(content)
            return t.render(context)
        
        except (VariableDoesNotExist, TemplateSyntaxError):
            return 'Error rendering', self.template

@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """
    Evaluate template tags in string value
    
    Usage:

        {% evaluate object.textfield %}
        {% evaluate object.textfield based 'base.html' %}

    Example:

        `flatpages/default.html`
            {% load evaluate_tag %}
            {% evaluate flatpage.content based 'base.html' %}
            
        flatpage content on db

            {% block head %}
            <title>{{ flatpage.title }}</title>
            {% endblock %}
            
            {% block content %}
            <h1>This is a test</h1>
            {% endblock %}

    """
    bits = token.split_contents()
    if len(bits) == 2:
        template = Variable(bits[1])
        based = None
    elif len(bits) == 4:
        if bits[2] != 'based':
            raise TemplateSyntaxError(
                    "second argument of %r tag must be 'based'" % bits[0]
                )
        template = Variable(bits[1])
        based = Variable(bits[3])
    else:
        raise TemplateSyntaxError("%r tag require exact two or four arguments" % bits[0])
    return EvaluateNode(template, based)

