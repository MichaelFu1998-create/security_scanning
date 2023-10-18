def _process_sasl_challenge(self, stream, element):
        """Process incoming <sasl:challenge/> element.

        [initiating entity only]
        """
        if not self.authenticator:
            logger.debug("Unexpected SASL challenge")
            return False

        content = element.text.encode("us-ascii")
        ret = self.authenticator.challenge(a2b_base64(content))
        if isinstance(ret, sasl.Response):
            element = ElementTree.Element(RESPONSE_TAG)
            element.text = ret.encode()
        else:
            element = ElementTree.Element(ABORT_TAG)

        stream.write_element(element)

        if isinstance(ret, sasl.Failure):
            stream.disconnect()
            raise SASLAuthenticationFailed("SASL authentication failed")

        return True