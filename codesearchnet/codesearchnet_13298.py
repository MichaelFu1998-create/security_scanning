def remove_item(self, jid, callback = None, error_callback = None):
        """Remove a contact from the roster.

        :Parameters:
            - `jid`: contact's jid
            - `callback`: function to call when the request succeeds. It should
              accept a single argument - a `RosterItem` describing the
              requested change
            - `error_callback`: function to call when the request fails. It
              should accept a single argument - an error stanza received
              (`None` in case of timeout)
        :Types:
            - `jid`: `JID`
        """
        item = self.roster[jid]
        if jid not in self.roster:
            raise KeyError(jid)
        item = RosterItem(jid, subscription = "remove")
        self._roster_set(item, callback, error_callback)