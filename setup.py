try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name = 'django_fabv',
    version = '0.1.0dev',
    url = 'https://pypi.python.org/pypi/django_fabv/0.1.0',
    include_package_data=True,
    packages=find_packages(),
    license = '3-clause BSD',
    author = 'Bob Jansen',
    author_email = 'bob.jansen@veneficus.nl',
    description = 'A/B module for Django based on ABingo',
    long_description=open('README').read(),
)
