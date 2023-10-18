def open511_convert(input_doc, output_format, serialize=True, **kwargs):
    """
    Convert an Open511 document between formats.
    input_doc - either an lxml open511 Element or a deserialized JSON dict
    output_format - short string name of a valid output format, as listed above
    """

    try:
        output_format_info = FORMATS[output_format]
    except KeyError:
        raise ValueError("Unrecognized output format %s" % output_format)

    input_doc = ensure_format(input_doc, output_format_info.input_format)

    result = output_format_info.func(input_doc, **kwargs)
    if serialize:
        result = output_format_info.serializer(result)
    return result