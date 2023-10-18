def _add_deprecated_function_notice_to_docstring(doc, date, instructions):
    """Adds a deprecation notice to a docstring for deprecated functions."""

    if instructions:
        deprecation_message = """
            .. warning::
                **THIS FUNCTION IS DEPRECATED:** It will be removed after %s.
                *Instructions for updating:* %s.
        """ % (('in a future version' if date is None else ('after %s' % date)), instructions)

    else:
        deprecation_message = """
            .. warning::
                **THIS FUNCTION IS DEPRECATED:** It will be removed after %s.
        """ % (('in a future version' if date is None else ('after %s' % date)))

    main_text = [deprecation_message]

    return _add_notice_to_docstring(doc, 'DEPRECATED FUNCTION', main_text)