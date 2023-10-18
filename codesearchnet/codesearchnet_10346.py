def to_unicode(obj):
    """Convert obj to unicode (if it can be be converted).

    Conversion is only attempted if `obj` is a string type (as
    determined by :data:`six.string_types`).

    .. versionchanged:: 0.7.0
       removed `encoding keyword argument

    """
    if not isinstance(obj, six.string_types):
        return obj

    try:
        obj = six.text_type(obj)
    except TypeError:
        pass
    return obj