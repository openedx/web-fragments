#!/usr/bin/env python
# pylint: disable=C0111,W6005,W6100
import os
import re
import sys

from setuptools import setup


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


VERSION = get_version('web_fragments', '__init__.py')

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), 'CHANGELOG.rst')).read()

setup(
    name='web-fragments',
    version=VERSION,
    description="""Web fragments""",
    long_description=README + '\n\n' + CHANGELOG,
    author='edX',
    author_email='oscm@edx.org',
    url='https://github.com/edx/web-fragments',
    packages=[
        'web_fragments',
    ],
    include_package_data=True,
    license="AGPL 3.0",
    zip_safe=False,
    keywords='Django edx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    extras_require={
        'Django': ['Django>=2.2,<2.3'],
    }
)
