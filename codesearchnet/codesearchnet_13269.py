def _process_sasl_response(self, stream, element):
        """Process incoming <sasl:response/> element.

        [receiving entity only]
        """
        if not self.authenticator:
            logger.debug("Unexpected SASL response")
            return False

        content = element.text.encode("us-ascii")
        ret = self.authenticator.response(a2b_base64(content))
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
            raise SASLAuthenticationFailed("SASL authentication failed: {0!r}"
                                                            .format(ret.reson))
        return True