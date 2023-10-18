def _process_sasl_abort(self, stream, element):
        """Process incoming <sasl:abort/> element.

        [receiving entity only]"""
        _unused, _unused = stream, element
        if not self.authenticator:
            logger.debug("Unexpected SASL response")
            return False

        self.authenticator = None
        logger.debug("SASL authentication aborted")
        return True