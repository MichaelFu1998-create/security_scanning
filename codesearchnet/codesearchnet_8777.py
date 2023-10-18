def add_generic_error_message_with_code(request, error_code):
    """
    Add message to request indicating that there was an issue processing request.

    Arguments:
        request: The current request.
        error_code: A string error code to be used to point devs to the spot in
                    the code where this error occurred.

    """
    messages.error(
        request,
        _(
            '{strong_start}Something happened.{strong_end} '
            '{span_start}Please reach out to your learning administrator with '
            'the following error code and they will be able to help you out.{span_end}'
            '{span_start}Error code: {error_code}{span_end}'
        ).format(
            error_code=error_code,
            strong_start='<strong>',
            strong_end='</strong>',
            span_start='<span>',
            span_end='</span>',
        )
    )