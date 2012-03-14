# vim: set fileencoding=utf-8 :
"""
Truncate letters filter works similar as 
truncatewords filter of builtin templatetags


Usage:

    {{ value|truncateletters:num }}
    {{ value|truncateletters_html:num }}



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
from django import template
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import re

register = template.Library()

def truncate_letters(s, num):
    "Truncates a string after a certain number of letters."
    if not s or s == "":
        return u""
    
    s = force_unicode(s)
    length = int(num)
    counter = 0
    for last, word in enumerate(s):
        if word in ('\n', '\r', '\s', '\t'): continue
        counter += 1
        if counter == length: break
    return s[:last+1] + (u'...' if last+1 < len(s) else '')
truncate_letters = allow_lazy(truncate_letters, unicode)

@register.filter
@stringfilter
def truncateletters(value, arg):
    """
    Truncates a string after a certain number of letters.

    Argument: Number of letters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return truncate_letters(value, length)
truncateletters.is_safe = True

def _find(value, start, last):
    last = value.find('>', start)
    last += 1
    return value[start:last]

def _isend(tag):
    r = re.compile("(?:<\s*/\s*[^>]*>)|(?:<[^/>]*/\s*>)")
    return not r.match(tag) is None

def _name(tag):
    r = re.compile("<\s*([^\s>]*)\s*.*?>")
    m = r.match(tag)
    return m.group(1) if m is not None else None

def truncate_html_letters(s, num):
    """
    Truncates html to a certain number of letters (not counting tags and
    comments). Closes opened tags if they were correctly closed in the given
    html.
    """
    if not s or s == "":
        return u""
    
    s = force_unicode(s)
    length = int(num)
    if length <= 0:
        return u''
    counter = 0
    skip = 0
    start_tags = []
    end_tags = []
    for last, word in enumerate(s):
        if skip > 0:
            skip -= 1
            continue
        elif word == '<':
            tag = _find(s, last, last)
            skip = len(tag) - 1
            if _isend(tag):
                end_tags.append(tag.translate(' \t'))
            else:
                start_tags.append(tag)
            continue
        elif word in ('\n', '\r', '\s', '\t'):
            continue
        counter += 1
        if counter == length:
            break
    suffix = ''
    for start_tag in start_tags:
        end_tag = "</%s>"%_name(start_tag)
        if not end_tag in end_tags:
            suffix = end_tag + suffix
        else:
            end_tags.remove(end_tag)
    suffix = '...' + suffix
    return mark_safe(s[:last+1].strip() + u'%s'%(suffix if last+1 < len(s) else ''))
truncate_html_letters = allow_lazy(truncate_html_letters, unicode)

@register.filter
@stringfilter
def truncateletters_html(value, arg):
    """
    Truncates HTML after a certain number of letters.

    Argument: Number of letters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    return truncate_html_letters(value, length)
truncateletters_html.is_safe = True
