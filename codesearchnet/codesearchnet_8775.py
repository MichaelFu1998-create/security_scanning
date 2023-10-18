def add_unenrollable_item_message(request, item):
    """
    Add a message to the Django message store indicating that the item (i.e. course run, program) is unenrollable.

    :param request: The current request.
    :param item: The item that is unenrollable (i.e. a course run).
    """
    messages.info(
        request,
        _(
            '{strong_start}Something happened.{strong_end} '
            '{span_start}This {item} is not currently open to new learners. Please start over and select a different '
            '{item}.{span_end}'
        ).format(
            item=item,
            strong_start='<strong>',
            strong_end='</strong>',
            span_start='<span>',
            span_end='</span>',
        )
    )