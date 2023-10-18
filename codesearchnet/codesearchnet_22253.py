def admin_obj_attr(obj, attr):
    """A safe version of :func:``utils.get_obj_attr`` that returns and empty
    string in the case of an exception or an empty object
    """
    try:
        field_obj = get_obj_attr(obj, attr)
        if not field_obj:
            return ''
    except AttributeError:
        return ''

    return field_obj