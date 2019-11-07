"""
URLs module
"""
from django.conf.urls import url

from campusromero_openedx_extensions.general_custom_views.api.v1.views import (
    ChangeToVerifiedMode,
)


urlpatterns = [  # pylint: disable=invalid-name
    # ITSoluciones
    url(
        r'^change_to_verified_mode/$',
        ChangeToVerifiedMode.as_view(),
        name='change_to_verified_mode'
    ),
]
