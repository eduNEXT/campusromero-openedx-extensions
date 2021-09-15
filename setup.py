#!/usr/bin/env python
"""
Setup file for campusromero-openedx-extensions Django plugin.
"""
import os
import re

import pip
from setuptools import setup


def get_version():
    """
    Retrieves the version string from __init__.py.
    """
    file_path = os.path.join("campusromero_openedx_extensions", "__init__.py")
    initfile_lines = open(file_path, "rt").readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        match_string = re.search(version_regex, line, re.M)
        if match_string:
            return match_string.group(1)
    raise RuntimeError("Unable to find version string in %s." % (file_path,))


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == ""
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
    )


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.strip() for line in open(path).readlines() if is_requirement(line)
        )
    return list(requirements)


setup(
    name="campusromero-openedx-extensions",
    version=get_version(),
    description="Custom OpenEdx extensions",
    author="eduNEXT",
    author_email="contact@edunext.co",
    packages=[
        "campusromero_openedx_extensions",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "lms.djangoapp": [
            "campusromero_openedx_extensions = campusromero_openedx_extensions.apps:CampusRomeroOpenedxExtensionsConfig",
        ],
        "cms.djangoapp": [
            "campusromero_openedx_extensions = campusromero_openedx_extensions.apps:CampusRomeroOpenedxExtensionsConfig",
        ],
    },
    install_requires=load_requirements("requirements/base.txt"),
)
