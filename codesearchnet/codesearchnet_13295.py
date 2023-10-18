def handle_roster_push(self, stanza):
        """Handle a roster push received from server.
        """
        if self.server is None and stanza.from_jid:
            logger.debug(u"Server address not known, cannot verify roster push"
                                " from {0}".format(stanza.from_jid))
            return stanza.make_error_response(u"service-unavailable")
        if self.server and stanza.from_jid and stanza.from_jid != self.server:
            logger.debug(u"Roster push from invalid source: {0}".format(
                                                            stanza.from_jid))
            return stanza.make_error_response(u"service-unavailable")
        payload = stanza.get_payload(RosterPayload)
        if len(payload) != 1:
            logger.warning("Bad roster push received ({0} items)"
                                                    .format(len(payload)))
            return stanza.make_error_response(u"bad-request")
        if self.roster is None:
            logger.debug("Dropping roster push - no roster here")
            return True
        item = payload[0]
        item.verify_roster_push(True)
        old_item = self.roster.get(item.jid)
        if item.subscription == "remove":
            if old_item:
                self.roster.remove_item(item.jid)
        else:
            self.roster.add_item(item, replace = True)
        self._event_queue.put(RosterUpdatedEvent(self, old_item, item))
        return stanza.make_result_response()