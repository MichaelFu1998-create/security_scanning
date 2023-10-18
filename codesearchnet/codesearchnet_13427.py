def _register_client_authenticator(klass, name):
    """Add a client authenticator class to `CLIENT_MECHANISMS_D`,
    `CLIENT_MECHANISMS` and, optionally, to `SECURE_CLIENT_MECHANISMS`
    """
    # pylint: disable-msg=W0212
    CLIENT_MECHANISMS_D[name] = klass
    items = sorted(CLIENT_MECHANISMS_D.items(), key = _key_func, reverse = True)
    CLIENT_MECHANISMS[:] = [k for (k, v) in items ]
    SECURE_CLIENT_MECHANISMS[:] = [k for (k, v) in items
                                                    if v._pyxmpp_sasl_secure]