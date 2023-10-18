def clear_cache(temp_dir=None):
    """
    Clears any cached info that was exported from the OS trust store. This will
    ensure the latest changes are returned from calls to get_list() and
    get_path(), but at the expense of re-exporting and parsing all certificates.

    :param temp_dir:
        The temporary directory to cache the CA certs in on OS X and Windows.
        Needs to have secure permissions so other users can not modify the
        contents. Must be the same value passed to get_path().
    """

    with memory_lock:
        _module_values['last_update'] = None
        _module_values['certs'] = None

    ca_path, temp = _ca_path(temp_dir)
    if temp:
        with path_lock:
            if os.path.exists(ca_path):
                os.remove(ca_path)