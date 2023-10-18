def _get_iq_handler(self, iq_type, payload):
        """Get an <iq/> handler for given iq  type and payload."""
        key = (payload.__class__, payload.handler_key)
        logger.debug("looking up iq {0} handler for {1!r}, key: {2!r}"
                            .format(iq_type, payload, key))
        logger.debug("handlers: {0!r}".format(self._iq_handlers))
        handler = self._iq_handlers[iq_type].get(key)
        return handler