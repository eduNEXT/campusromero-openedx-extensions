"""
Common settings for campusromero_openedx_extensions project.
"""
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'campusromero_openedx_extensions.custom_registration_form'
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Settings for custom registration form.
    settings.REGISTRATION_EXTENSION_FORM = "campusromero_openedx_extensions.custom_registration_form.forms.CustomForm"
    settings.ADDL_INSTALLED_APPS = getattr(settings, 'ADDL_INSTALLED_APPS', [])
    settings.ADDL_INSTALLED_APPS.append("campusromero_openedx_extensions.custom_registration_form")
    settings.ADDL_INSTALLED_APPS.append("campusromero_openedx_extensions.user_import_export")
    settings.ENABLE_COMBINED_LOGIN_REGISTRATION = True
    # Settings for QRcode certificates
    settings.CERTIFICATES_QR_CODE_BUCKET = "stage-cromero-certificates-qrcodes"
    settings.CERTIFICATES_QR_CODE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
    settings.CAMPUS_EDXMAKO_MODULE = "campusromero_openedx_extensions.edxapp_wrapper.backends.edxmako_campus_module"
