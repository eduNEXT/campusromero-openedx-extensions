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
            u'lms.djangoapp': {
                u'common': {'relative_path': u'settings.common'},
            },
            'cms.djangoapp': {},
        },
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'general_custom_views',
                'relative_path': 'general_custom_views.urls',
            }
        },
    }
