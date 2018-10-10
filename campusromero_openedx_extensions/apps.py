"""
File configuration for campusromero_openedx_extensions.
"""
from django.apps import AppConfig

class CampusRomeroOpenedxExtensionsConfig(AppConfig):
    """
    App configuration.
    """
    name = 'campusromero_openedx_extensions'
    verbose_name = "Campus Romero Openedx Extensions"

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {},
            'cms.djangoapp': {},
        },
    }
