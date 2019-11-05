
"""
Settings for campusromero_openedx_extensions
"""

from __future__ import absolute_import, unicode_literals

from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """

    # Preventing clashes with already added installed apps
    PLUGIN_INSTALLED_APPS = [
        "campusromero_openedx_extensions.custom_registration_form",
    ]

    for single_app in PLUGIN_INSTALLED_APPS:
        if single_app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.append(single_app)
    settings.AWS_STORAGE_BUCKET_NAME = 'test-certificate'
