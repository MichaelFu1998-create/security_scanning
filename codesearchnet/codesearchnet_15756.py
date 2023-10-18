def domain_name():
    """Return a random domain name.

    Lowercased result of :py:func:`~forgery_py.forgery.name.company_name()`
    plus :py:func:`~top_level_domain()`.
    """
    result = random.choice(get_dictionary('company_names')).strip()
    result += '.' + top_level_domain()

    return result.lower()