def email_address(user=None):
    """Return random e-mail address in a hopefully imaginary domain.

    If `user` is ``None`` :py:func:`~user_name()` will be used. Otherwise it
    will be lowercased and will have spaces replaced with ``_``.

    Domain name is created using :py:func:`~domain_name()`.
    """
    if not user:
        user = user_name()
    else:
        user = user.strip().replace(' ', '_').lower()

    return user + '@' + domain_name()