def get_user_from_context(context):
    """
    Get the user instance from the template context, if possible.

    If the context does not contain a `request` or `user` attribute,
    `None` is returned.
    """
    try:
        return context['user']
    except KeyError:
        pass
    try:
        request = context['request']
        return request.user
    except (KeyError, AttributeError):
        pass
    return None