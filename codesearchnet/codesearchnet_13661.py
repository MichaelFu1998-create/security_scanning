def _post_auth(self):
        """Unregister legacy authentication handlers after successfull
        authentication."""
        ClientStream._post_auth(self)
        if not self.initiator:
            self.unset_iq_get_handler("query","jabber:iq:auth")
            self.unset_iq_set_handler("query","jabber:iq:auth")