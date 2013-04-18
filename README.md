# Introduction #

fabv enables you to setup A/B testing for your Django projects easily
and quickly. It is based on Patrick McKenzies ABingo for Ruby.

# License #

fabv is licensed under the 3-clause BSD license.

# Why fabv #
- Easy to use and setup
- No dependencies (except Django)

# Installation #
Install the app using pip:

	pip install django_fabv

and change your settings as follows:

1. Add `'django.core.context_processors.request'` to
   `TEMPLATE_CONTEXT_PROCESSORS`;
2. add `'django_fabv.middleware.FabvMiddleware'` to
   `MIDDLEWARE_CLASSES` and
3. add `'django_fabv'` to `INSTALLED_APPS`.

# Contribute and TODO #
- Add test for more than two alternatives
- Support changing of complete templates instead of parts throught tags
- Better django-admin support
- Figure out database error (Lines marked TODO in middleware.py)
