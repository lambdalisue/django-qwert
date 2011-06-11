``django-qwert`` is django's snippets collection by Alisue
each snippets' has different author so please checkout the link on the each file's comment.
(some code is written by me or couldn't find source url)

Install
===========================================
::

	sudo pip install django-qwert

or::

    sudo pip install git+git://github.com/lambdalisue/django-qwert.git#egg=django-qwert


Features
==========================================

+	Http403 Exception
	http://chronosbox.org/blog/manipulando-erros-http-403-permissao-negada-no-django?lang=en
+	User based exception
	http://djangosnippets.org/snippets/935/
+	Thread local (global request)
+	Automatically generate test user on syncdb when DEBUG=True
    http://stackoverflow.com/questions/1466827/
+	Protect comment post from spam using Akismet
+	Useful templatetags

	+	smart_if
	+	expr
	+	evaluate_tag
	+	get_archives
	+	get_latest
	+	get_links
	+	markdown_tags
	+	truncateletters
	+	urlize_html

Required
=========================================
+	BeautifulSoup
+	Akismet
+	markdown

Settings
=========================================

Automatically generate test user on syncdb when DEBUG=True
----------------------------------------------------------
``AUTO_CREATE_USER``
	When it ``True`` then create test user (username: admin, password: admin) automatically when syncdb is running.
	the default value is ``True``

Protect comment post from spam using Akismet
----------------------------------------------------------
``AKISMET_COMMENT_PROTECT``
	When it ``True`` then protecting comment post by Akismet feature is enable. the default value is ``True``

``TYPEPAD_ANTISPAM_API_KEY``
	When it is setted using Typepad antispam is used for protecting comment

``AKISMET_API_KEY``
	Required to set for enabling protecting feature.
