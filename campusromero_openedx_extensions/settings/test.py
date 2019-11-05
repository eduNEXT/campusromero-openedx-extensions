
"""
Settings for campusromero_openedx_extensions
"""

from __future__ import absolute_import, unicode_literals

from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """

    # Preventing clashes with already added installed apps
    plugin_installed_apps = [
        "campusromero_openedx_extensions.custom_registration_form",
    ]

    for single_app in plugin_installed_apps:
        if single_app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.append(single_app)
    settings.AWS_STORAGE_BUCKET_NAME = 'test-certificate'
