def parse(text, encoding='utf8'):
    """Parse the querystring into a normalized form."""

    # Decode the text if we got bytes.
    if isinstance(text, six.binary_type):
        text = text.decode(encoding)

    return Query(text, split_segments(text))