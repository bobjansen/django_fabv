from distutils.core import setup


setup(
    name = 'django_fabv',
    version = '0.1.0',
    packages = ['django_fabv',],
    license = '3-clause BSD',
    author = 'Bob Jansen',
    author_email = 'bob.jansen@veneficus.nl',
    description = 'A/B module for Django based on ABingo',
    long_description=open('README.md').read(),
)
