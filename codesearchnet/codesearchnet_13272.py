def _process_sasl_failure(self, stream, element):
        """Process incoming <sasl:failure/> element.

        [initiating entity only]
        """
        _unused = stream
        if not self.authenticator:
            logger.debug("Unexpected SASL response")
            return False

        logger.debug("SASL authentication failed: {0!r}".format(
                                                element_to_unicode(element)))
        raise SASLAuthenticationFailed("SASL authentication failed")