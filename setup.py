#!/usr/bin/env python
"""
Setup file for campusromero-openedx-extensions Django plugin.
"""
import os
import re
from distutils.core import setup


def get_version():
    """
    Retrives the version string from __init__.py.
    """
    file_path = os.path.join('campusromero_openedx_extensions', '__init__.py')
    initfile_lines = open(file_path, 'rt').readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        match_string = re.search(version_regex, line, re.M)
        if match_string:
            return match_string.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (file_path,))

setup(
    name='campusromero-openedx-extensions',
    version=get_version(),
    description='Custom OpenEdx extensions',
    author='eduNEXT',
    author_email='contact@edunext.co',
    packages=['campusromero_openedx_extensions'],
    zip_safe=False,
    entry_points={
        "lms.djangoapp": [
            "campusromero_openedx_extensions = campusromero_openedx_extensions.apps:CampusRomeroOpenedxExtensionsConfig",
        ],
        "cms.djangoapp": [
            "campusromero_openedx_extensions = campusromero_openedx_extensions.apps:CampusRomeroOpenedxExtensionsConfig",
        ],
    }
)
