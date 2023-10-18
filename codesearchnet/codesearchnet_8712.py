def get_global_context(request, enterprise_customer):
    """
    Get the set of variables that are needed by default across views.
    """
    platform_name = get_configuration_value("PLATFORM_NAME", settings.PLATFORM_NAME)
    # pylint: disable=no-member
    return {
        'enterprise_customer': enterprise_customer,
        'LMS_SEGMENT_KEY': settings.LMS_SEGMENT_KEY,
        'LANGUAGE_CODE': get_language_from_request(request),
        'tagline': get_configuration_value("ENTERPRISE_TAGLINE", settings.ENTERPRISE_TAGLINE),
        'platform_description': get_configuration_value(
            "PLATFORM_DESCRIPTION",
            settings.PLATFORM_DESCRIPTION,
        ),
        'LMS_ROOT_URL': settings.LMS_ROOT_URL,
        'platform_name': platform_name,
        'header_logo_alt_text': _('{platform_name} home page').format(platform_name=platform_name),
        'welcome_text': constants.WELCOME_TEXT.format(platform_name=platform_name),
        'enterprise_welcome_text': constants.ENTERPRISE_WELCOME_TEXT.format(
            enterprise_customer_name=enterprise_customer.name,
            platform_name=platform_name,
            strong_start='<strong>',
            strong_end='</strong>',
            line_break='<br/>',
            privacy_policy_link_start="<a href='{pp_url}' target='_blank'>".format(
                pp_url=get_configuration_value('PRIVACY', 'https://www.edx.org/edx-privacy-policy', type='url'),
            ),
            privacy_policy_link_end="</a>",
        ),
    }