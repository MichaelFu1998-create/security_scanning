def _sasl_authenticate(self, stream, username, authzid):
        """Start SASL authentication process.

        [initiating entity only]

        :Parameters:
            - `username`: user name.
            - `authzid`: authorization ID.
            - `mechanism`: SASL mechanism to use."""
        if not stream.initiator:
            raise SASLAuthenticationFailed("Only initiating entity start"
                                                        " SASL authentication")
        if stream.features is None or not self.peer_sasl_mechanisms:
            raise SASLNotAvailable("Peer doesn't support SASL")

        props = dict(stream.auth_properties)
        if not props.get("service-domain") and (
                                        stream.peer and stream.peer.domain):
            props["service-domain"] = stream.peer.domain
        if username is not None:
            props["username"] = username
        if authzid is not None:
            props["authzid"] = authzid
        if "password" in self.settings:
            props["password"] = self.settings["password"]
        props["available_mechanisms"] = self.peer_sasl_mechanisms
        enabled = sasl.filter_mechanism_list(
                            self.settings['sasl_mechanisms'], props,
                                            self.settings['insecure_auth'])
        if not enabled:
            raise SASLNotAvailable(
                                "None of SASL mechanism selected can be used")
        props["enabled_mechanisms"] = enabled

        mechanism = None
        for mech in enabled:
            if mech in self.peer_sasl_mechanisms:
                mechanism = mech
                break
        if not mechanism:
            raise SASLMechanismNotAvailable("Peer doesn't support any of"
                                                    " our SASL mechanisms")
        logger.debug("Our mechanism: {0!r}".format(mechanism))

        stream.auth_method_used = mechanism
        self.authenticator = sasl.client_authenticator_factory(mechanism)
        initial_response = self.authenticator.start(props)
        if not isinstance(initial_response, sasl.Response):
            raise SASLAuthenticationFailed("SASL initiation failed")

        element = ElementTree.Element(AUTH_TAG)
        element.set("mechanism", mechanism)
        if initial_response.data:
            if initial_response.encode:
                element.text = initial_response.encode()
            else:
                element.text = initial_response.data
        stream.write_element(element)