def _get_error(self, stanza):
        """Handle failure of the roster request.
        """
        if stanza:
            logger.debug(u"Roster request failed: {0}".format(
                                                stanza.error.condition_name))
        else:
            logger.debug(u"Roster request failed: timeout")
        self._event_queue.put(RosterNotReceivedEvent(self, stanza))