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
            'lms.djangoapp': {
                'production': {'relative_path': 'settings.production'},
                'common': {'relative_path': 'settings.common'},
                'devstack': {'relative_path': 'settings.devstack'},
                'test': {'relative_path': 'settings.test'},
            },
            'cms.djangoapp': {
                'production': {'relative_path': 'settings.production'},
                'common': {'relative_path': 'settings.common'},
                'devstack': {'relative_path': 'settings.devstack'},
                'test': {'relative_path': 'settings.test'},
            },
        },
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'general_custom_views',
                'relative_path': 'general_custom_views.urls',
            }
        },
    }
