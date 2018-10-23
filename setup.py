#!/usr/bin/env python
"""
Setup file for campusromero-openedx-extensions Django plugin.
"""
import os
import re
from distutils.core import setup
import pip


REQUIREMENTS_ENVS = [
    "dev",
    "prod"
]


def get_version():
    """
    Retrieves the version string from __init__.py.
    """
    file_path = os.path.join('campusromero_openedx_extensions', '__init__.py')
    initfile_lines = open(file_path, 'rt').readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        match_string = re.search(version_regex, line, re.M)
        if match_string:
            return match_string.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (file_path,))


def get_requirements(env="prod"):
    """
    Retrieves the requirements for this plugin
    """
    links = []
    requires = []

    if env not in REQUIREMENTS_ENVS:
        return links, requires

    filename_reqs = "requirements/{}.txt".format(env)
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        filename_reqs,
        session=pip.download.PipSession()
    )

    for item in requirements:
        # we want to handle package names and also repo urls
        if getattr(item, "url", None):  # older pip has url
            links.append(str(item.url))
        if getattr(item, "link", None):  # newer pip has link
            links.append(str(item.link))
        if item.req:
            requires.append(str(item.req))

    return links, requires


links, requires = get_requirements()


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
    },
    install_requires=requires,
    dependency_links=links
)
