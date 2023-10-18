def field_size_limit(limit=undefined):
    """Sets an upper limit on parsed fields.
    csv.field_size_limit([limit])

    Returns old limit. If limit is not given, no new limit is set and
    the old limit is returned"""

    global _field_limit
    old_limit = _field_limit

    if limit is not undefined:
        if not isinstance(limit, (int, long)):
            raise TypeError("int expected, got %s" %
                            (limit.__class__.__name__,))
        _field_limit = limit

    return old_limit