def user_name(with_num=False):
    """Return a random user name.

    Basically it's lowercased result of
    :py:func:`~forgery_py.forgery.name.first_name()` with a number appended
    if `with_num`.
    """
    result = first_name()
    if with_num:
        result += str(random.randint(63, 94))

    return result.lower()