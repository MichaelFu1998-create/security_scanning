def add_item(self, jid, name = None, groups = None,
                                callback = None, error_callback = None):
        """Add a contact to the roster.

        :Parameters:
            - `jid`: contact's jid
            - `name`: name for the contact
            - `groups`: sequence of group names the contact should belong to
            - `callback`: function to call when the request succeeds. It should
              accept a single argument - a `RosterItem` describing the
              requested change
            - `error_callback`: function to call when the request fails. It
              should accept a single argument - an error stanza received
              (`None` in case of timeout)
        :Types:
            - `jid`: `JID`
            - `name`: `unicode`
            - `groups`: sequence of `unicode`
        """
        # pylint: disable=R0913
        if jid in self.roster:
            raise ValueError("{0!r} already in the roster".format(jid))
        item = RosterItem(jid, name, groups)
        self._roster_set(item, callback, error_callback)