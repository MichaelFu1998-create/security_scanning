def add_missing_price_information_message(request, item):
    """
    Add a message to the Django messages store indicating that we failed to retrieve price information about an item.

    :param request: The current request.
    :param item: The item for which price information is missing. Example: a program title, or a course.
    """
    messages.warning(
        request,
        _(
            '{strong_start}We could not gather price information for {em_start}{item}{em_end}.{strong_end} '
            '{span_start}If you continue to have these issues, please contact '
            '{link_start}{platform_name} support{link_end}.{span_end}'
        ).format(
            item=item,
            em_start='<em>',
            em_end='</em>',
            link_start='<a href="{support_link}" target="_blank">'.format(
                support_link=get_configuration_value('ENTERPRISE_SUPPORT_URL', settings.ENTERPRISE_SUPPORT_URL),
            ),
            platform_name=get_configuration_value('PLATFORM_NAME', settings.PLATFORM_NAME),
            link_end='</a>',
            span_start='<span>',
            span_end='</span>',
            strong_start='<strong>',
            strong_end='</strong>',
        )
    )