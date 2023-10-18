def _get_success(self, stanza):
        """Handle successful response to the roster request.
        """
        payload = stanza.get_payload(RosterPayload)
        if payload is None:
            if "versioning" in self.server_features and self.roster:
                logger.debug("Server will send roster delta in pushes")
            else:
                logger.warning("Bad roster response (no payload)")
                self._event_queue.put(RosterNotReceivedEvent(self, stanza))
                return
        else:
            items = list(payload)
            for item in items:
                item.verify_roster_result(True)
            self.roster = Roster(items, payload.version)
        self._event_queue.put(RosterReceivedEvent(self, self.roster))