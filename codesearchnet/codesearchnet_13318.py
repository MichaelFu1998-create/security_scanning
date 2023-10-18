def make_join_request(self, password = None, history_maxchars = None,
            history_maxstanzas = None, history_seconds = None,
            history_since = None):
        """
        Make the presence stanza a MUC room join request.

        :Parameters:
            - `password`: password to the room.
            - `history_maxchars`: limit of the total number of characters in
              history.
            - `history_maxstanzas`: limit of the total number of messages in
              history.
            - `history_seconds`: send only messages received in the last
              `seconds` seconds.
            - `history_since`: Send only the messages received since the
              dateTime specified (UTC).
        :Types:
            - `password`: `unicode`
            - `history_maxchars`: `int`
            - `history_maxstanzas`: `int`
            - `history_seconds`: `int`
            - `history_since`: `datetime.datetime`
        """
        self.clear_muc_child()
        self.muc_child=MucX(parent=self.xmlnode)
        if (history_maxchars is not None or history_maxstanzas is not None
                or history_seconds is not None or history_since is not None):
            history = HistoryParameters(history_maxchars, history_maxstanzas,
                    history_seconds, history_since)
            self.muc_child.set_history(history)
        if password is not None:
            self.muc_child.set_password(password)