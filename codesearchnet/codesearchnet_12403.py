def format(obj, options):
    """Return a string representation of the Python object

    Args:
        obj: The Python object
        options: Format options
    """
    formatters = {
        float_types: lambda x: '{:.{}g}'.format(x, options.digits),
    }
    for _types, fmtr in formatters.items():
        if isinstance(obj, _types):
            return fmtr(obj)
    try:
        if six.PY2 and isinstance(obj, six.string_types):
            return str(obj.encode('utf-8'))
        return str(obj)
    except:
        return 'OBJECT'