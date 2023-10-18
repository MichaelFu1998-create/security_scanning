def get_identity(context, prefix=None, identity_func=None, user=None):
    """
    Get the identity of a logged in user from a template context.

    The `prefix` argument is used to provide different identities to
    different analytics services.  The `identity_func` argument is a
    function that returns the identity of the user; by default the
    identity is the username.
    """
    if prefix is not None:
        try:
            return context['%s_identity' % prefix]
        except KeyError:
            pass
    try:
        return context['analytical_identity']
    except KeyError:
        pass
    if getattr(settings, 'ANALYTICAL_AUTO_IDENTIFY', True):
        try:
            if user is None:
                user = get_user_from_context(context)
            if get_user_is_authenticated(user):
                if identity_func is not None:
                    return identity_func(user)
                else:
                    return user.get_username()
        except (KeyError, AttributeError):
            pass
    return None