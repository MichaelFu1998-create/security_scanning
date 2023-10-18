def add_generic_info_message_for_error(request):
    """
    Add message to request indicating that there was an issue processing request.

    Arguments:
        request: The current request.

    """
    messages.info(
        request,
        _(
            '{strong_start}Something happened.{strong_end} '
            '{span_start}This course link is currently invalid. '
            'Please reach out to your Administrator for assistance to this course.{span_end}'
        ).format(
            span_start='<span>',
            span_end='</span>',
            strong_start='<strong>',
            strong_end='</strong>',
        )
    )