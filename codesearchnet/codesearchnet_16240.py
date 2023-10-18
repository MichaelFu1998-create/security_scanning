def split_docstring(value):
    """
    Splits the docstring of the given value into it's summary and body.

    :returns: a 2-tuple of the format ``(summary, body)``
    """
    docstring = textwrap.dedent(getattr(value, '__doc__', ''))
    if not docstring:
        return None

    pieces = docstring.strip().split('\n\n', 1)
    try:
        body = pieces[1]
    except IndexError:
        body = None

    return Docstring(pieces[0], body)