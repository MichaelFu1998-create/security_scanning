def _process_tls_proceed(self, stream, element):
        """Handle the <proceed /> element.
        """
        # pylint: disable-msg=W0613
        if not self.requested:
            logger.debug("Unexpected TLS element: {0!r}".format(element))
            return False
        logger.debug(" tls: <proceed/> received")
        self.requested = False
        self._make_tls_connection()
        return True