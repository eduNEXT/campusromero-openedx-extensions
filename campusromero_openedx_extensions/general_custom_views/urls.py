"""
Urls module used in the camrom plugin.
"""
from django.conf.urls import url
from django.conf import settings

from campusromero_openedx_extensions.general_custom_views.views import (
    iframe_log_reg,
    purchase_course,
    change_enrollment,
    noLogingVerified,
    noLoginBasket,
    contactanos,
)


urlpatterns = [  # pylint: disable=invalid-name
    # ITSoluciones
    url(r'^iframe_button_log_reg$', iframe_log_reg, name="iframe_log_reg"),
    url(
        r'^purchase_course/{}/enroll$'.format(settings.COURSE_ID_PATTERN),
        purchase_course,
        name="purchase_course"
    ),
    url(
        r'^purchase_course/{}/change_enrollment$'.format(settings.COURSE_ID_PATTERN),
        change_enrollment,
        name="change_enrollment"
    ),

    # MagiaDigital - VD
    url(
        r'^purchase_course/{}/redirectVerified$'.format(settings.COURSE_ID_PATTERN),
        noLogingVerified,
        name="noLogingVerified"
    ),
    url(r'^purchase_course/(?P<sku>[^/]*)/redirect$', noLoginBasket, name="noLoginBasket"),

    # Contact us view
    url(r'^contactanos$', contactanos.as_view(), name='contactanos'),
]
