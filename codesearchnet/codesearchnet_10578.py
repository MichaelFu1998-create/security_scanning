def set_defaults(key):
    """
    Load a default value for redshift from config and set it as the redshift for source or lens galaxies that have
    falsey redshifts

    Parameters
    ----------
    key: str

    Returns
    -------
    decorator
        A decorator that wraps the setter function to set defaults
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(phase, new_value):
            new_value = new_value or []
            for item in new_value:
                # noinspection PyTypeChecker
                galaxy = new_value[item] if isinstance(item, str) else item
                galaxy.redshift = galaxy.redshift or conf.instance.general.get("redshift", key, float)
            return func(phase, new_value)

        return wrapper

    return decorator