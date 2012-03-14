# vim: set fileencoding=utf-8 :
from setuptools import setup, find_packages

version = __import__('qwert').__version__

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

def readlist(filename):
    import os.path
    app_list = open(os.path.join(os.path.dirname(__file__), filename)).readlines()
    app_list = map((lambda x: None if x.startswith('#') else x.strip()), app_list)
    app_list = filter(bool, app_list)
    return app_list

setup(
    name="django-qwert",
    version=version,
    description = "A trivia collection framework for Django",
    long_description=read('README.rst'),
    classifiers = [
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django trivia snipet collection framework",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-qwert",
    download_url = r"https://github.com/lambdalisue/django-qwert/tarball/master",
    license = 'MIT',
    zip_safe=False,
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    test_suite='runtests.runtests',
    tests_require=readlist('requirements-test.txt'),
    install_requires=readlist('requirements.txt'),
)
