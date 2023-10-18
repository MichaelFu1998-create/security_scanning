def sasl_mechanism(name, secure, preference = 50):
    """Class decorator generator for `ClientAuthenticator` or
    `ServerAuthenticator` subclasses. Adds the class to the pyxmpp.sasl
    mechanism registry.

    :Parameters:
        - `name`: SASL mechanism name
        - `secure`: if the mechanims can be considered secure - `True`
          if it can be used over plain-text channel
        - `preference`: mechanism preference level (the higher the better)
    :Types:
        - `name`: `unicode`
        - `secure`: `bool`
        - `preference`: `int`
    """
    # pylint: disable-msg=W0212
    def decorator(klass):
        """The decorator."""
        klass._pyxmpp_sasl_secure = secure
        klass._pyxmpp_sasl_preference = preference
        if issubclass(klass, ClientAuthenticator):
            _register_client_authenticator(klass, name)
        elif issubclass(klass, ServerAuthenticator):
            _register_server_authenticator(klass, name)
        else:
            raise TypeError("Not a ClientAuthenticator"
                                            " or ServerAuthenticator class")
        return klass
    return decorator