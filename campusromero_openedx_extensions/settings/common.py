"""
Common settings for campusromero_openedx_extensions project.
"""
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'campusromero_openedx_extensions.custom_registration_form'
]

TIME_ZONE = 'UTC'


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Settings for QRcode certificates
    settings.CERTIFICATES_QR_CODE_BUCKET = "qrcodes-test-bucket"
    settings.CERTIFICATES_QR_CODE_STORAGE = (
        "campusromero_openedx_extensions.certificates.storage.CertificatesQRCodeS3Storage"
    )
    settings.CAMPUS_EDXMAKO_MODULE = "campusromero_openedx_extensions.edxapp_wrapper.backends.edxmako_campus_module"  # pylint: disable=line-too-long
    settings.CAMPUS_VERIFYSTUDENT_MODULE = "campusromero_openedx_extensions.edxapp_wrapper.backends.i_verify_student"  # pylint: disable=line-too-long
