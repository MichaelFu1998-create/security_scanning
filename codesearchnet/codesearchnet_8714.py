def render_page_with_error_code_message(request, context_data, error_code, log_message):
    """
    Return a 404 page with specified error_code after logging error and adding message to django messages.
    """
    LOGGER.error(log_message)
    messages.add_generic_error_message_with_code(request, error_code)
    return render(
        request,
        ENTERPRISE_GENERAL_ERROR_PAGE,
        context=context_data,
        status=404,
    )