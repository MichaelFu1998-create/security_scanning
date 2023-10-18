def init_backend(limit=None):
    """
    Load a keyring specified in the config file or infer the best available.

    Limit, if supplied, should be a callable taking a backend and returning
    True if that backend should be included for consideration.
    """
    # save the limit for the chainer to honor
    backend._limit = limit

    # get all keyrings passing the limit filter
    keyrings = filter(limit, backend.get_all_keyring())

    set_keyring(
        load_env()
        or load_config()
        or max(keyrings, default=fail.Keyring(), key=backend.by_priority)
    )