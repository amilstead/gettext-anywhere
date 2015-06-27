from setuptools import setup
from setuptools import find_packages


with open('VERSION') as _file:
    VERSION = _file.readline().rstrip('\n')


setup(
    name='gettext-anywhere',
    version=VERSION,
    description='Register gettext catalog files from anywhere.',
    author='Alex Milstead',
    author_email='alex@amilstead.com',
    url='https://github.com/amilstead/gettext-anywhere',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests']),
    test_suite='tests'
)
