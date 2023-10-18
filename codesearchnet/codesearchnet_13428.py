def _register_server_authenticator(klass, name):
    """Add a client authenticator class to `SERVER_MECHANISMS_D`,
    `SERVER_MECHANISMS` and, optionally, to `SECURE_SERVER_MECHANISMS`
    """
    # pylint: disable-msg=W0212
    SERVER_MECHANISMS_D[name] = klass
    items = sorted(SERVER_MECHANISMS_D.items(), key = _key_func, reverse = True)
    SERVER_MECHANISMS[:] = [k for (k, v) in items ]
    SECURE_SERVER_MECHANISMS[:] = [k for (k, v) in items
                                                    if v._pyxmpp_sasl_secure]