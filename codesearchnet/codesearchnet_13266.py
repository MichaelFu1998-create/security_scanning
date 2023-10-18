def process_sasl_auth(self, stream, element):
        """Process incoming <sasl:auth/> element.

        [receiving entity only]
        """
        if self.authenticator:
            logger.debug("Authentication already started")
            return False

        password_db = self.settings["password_database"]
        mechanism = element.get("mechanism")
        if not mechanism:
            stream.send_stream_error("bad-format")
            raise FatalStreamError("<sasl:auth/> with no mechanism")

        stream.auth_method_used = mechanism
        self.authenticator = sasl.server_authenticator_factory(mechanism,
                                                                password_db)

        content = element.text.encode("us-ascii")
        ret = self.authenticator.start(stream.auth_properties,
                                                a2b_base64(content))

        if isinstance(ret, sasl.Success):
            element = ElementTree.Element(SUCCESS_TAG)
            element.text = ret.encode()
        elif isinstance(ret, sasl.Challenge):
            element = ElementTree.Element(CHALLENGE_TAG)
            element.text = ret.encode()
        else:
            element = ElementTree.Element(FAILURE_TAG)
            ElementTree.SubElement(element, SASL_QNP + ret.reason)

        stream.write_element(element)

        if isinstance(ret, sasl.Success):
            self._handle_auth_success(stream, ret)
        elif isinstance(ret, sasl.Failure):
            raise SASLAuthenticationFailed("SASL authentication failed: {0}"
                                                            .format(ret.reason))
        return True