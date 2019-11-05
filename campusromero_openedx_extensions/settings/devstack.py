"""
devstack settings for campusromero_openedx_extensions project.
This settings are intended to ease the configuration of some features
for devs working in this feature
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info:
    https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Setting the installed apps inside the campus romero plugin.
    # Please add those ones via ansible to ADDL_INSTALLED_APPS on production environment
    settings.INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

    # Preventing clashes with already added installed apps
    PLUGIN_INSTALLED_APPS = [
        "campusromero_openedx_extensions.custom_registration_form",
        "campusromero_openedx_extensions.user_import_export",
        "import_export",
        "rangefilter",
    ]

    for single_app in PLUGIN_INSTALLED_APPS:
        if single_app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.append(single_app)

    # Settings for custom registration form.
    # Please add this via ansible on prod environments
    settings.REGISTRATION_EXTENSION_FORM = "campusromero_openedx_extensions.custom_registration_form.forms.CustomForm"  # pylint: disable=line-too-long
    settings.ENABLE_COMBINED_LOGIN_REGISTRATION = True
