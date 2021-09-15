"""
production settings for campusromero_openedx_extensions project.
"""
from __future__ import absolute_import, unicode_literals


def plugin_settings(settings):
    """
    Defines seb_openedx settings when app is used as a plugin to edx-platform.
    See: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """

    settings.CERTIFICATES_QR_CODE_BUCKET = getattr(
        settings, 'ENV_TOKENS', {}
    ).get('CERTIFICATES_QR_CODE_BUCKET', getattr(
        settings, "CERTIFICATES_QR_CODE_BUCKET"
    ))

    settings.CERTIFICATES_QR_CODE_STORAGE = getattr(
        settings, 'ENV_TOKENS', {}
    ).get('CERTIFICATES_QR_CODE_STORAGE', getattr(
        settings, "CERTIFICATES_QR_CODE_STORAGE"
    ))

    settings.CAMPUS_EDXMAKO_MODULE = getattr(
        settings, 'ENV_TOKENS', {}
    ).get('CAMPUS_EDXMAKO_MODULE', getattr(
        settings, "CAMPUS_EDXMAKO_MODULE"
    ))
