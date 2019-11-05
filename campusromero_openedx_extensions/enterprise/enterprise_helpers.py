"""
Helpers to access the enterprise app.
"""
import logging

ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS = 'enterprise_customer_branding_override_details'
LOGGER = logging.getLogger("campusromero_openedx_extensions.enterprise.enterprise_helpers")


def set_enterprise_branding_filter_param(request, provider_id):
    """
    Setting 'ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS' in session.
    'ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS' either be provider_id or
    ec_uuid. e.g. {provider_id: 'xyz'} or {ec_src: enterprise_customer_uuid}
    """
    ec_uuid = request.GET.get('ec_src', None)
    if provider_id:
        LOGGER.info(
            "Session key 'ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS' "
            "has been set with provider_id '%s'",
            provider_id
        )
        request.session[ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS] = {
            'provider_id': provider_id
        }

    elif ec_uuid:
        # we are assuming that none sso based enterprise will return
        # Enterprise Customer uuid as 'ec_src' in query
        # param e.g. edx.org/foo/bar?ec_src=6185ed46-68a4-45d6-8367-96c0bf70d1a6
        LOGGER.info(
            "Session key 'ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS' "
            "has been set with ec_uuid '%s'",
            ec_uuid
        )
        request.session[ENTERPRISE_CUSTOMER_BRANDING_OVERRIDE_DETAILS] = {'ec_uuid': ec_uuid}
