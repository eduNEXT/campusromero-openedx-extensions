""" urls.py """

from django.conf.urls import url, include


urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^v1/',
        include(
            ('campusromero_openedx_extensions.general_custom_views.api.v1.urls',
            'camrom-api'),
            namespace='camrom-api',
        )
    ),
]
