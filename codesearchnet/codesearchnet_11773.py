def str_to_list(s):
    """
    Converts a string of comma delimited values and returns a list.
    """
    if s is None:
        return []
    elif isinstance(s, (tuple, list)):
        return s
    elif not isinstance(s, six.string_types):
        raise NotImplementedError('Unknown type: %s' % type(s))
    return [_.strip().lower() for _ in (s or '').split(',') if _.strip()]