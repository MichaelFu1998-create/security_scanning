def update_item(self, jid, name = NO_CHANGE, groups = NO_CHANGE,
                                callback = None, error_callback = None):
        """Modify a contact in the roster.

        :Parameters:
            - `jid`: contact's jid
            - `name`: a new name for the contact
            - `groups`: a sequence of group names the contact should belong to
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
        item = self.roster[jid]
        if name is NO_CHANGE and groups is NO_CHANGE:
            return
        if name is NO_CHANGE:
            name = item.name
        if groups is NO_CHANGE:
            groups = item.groups
        item = RosterItem(jid, name, groups)
        self._roster_set(item, callback, error_callback)