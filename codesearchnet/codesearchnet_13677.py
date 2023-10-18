def registration_success(self, stanza):
        """Handle registration success.

        [client only]

        Clean up registration stuff, change state to "registered" and initialize
        authentication.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `pyxmpp.iq.Iq`"""
        _unused = stanza
        self.lock.acquire()
        try:
            self.state_change("registered", self.registration_form)
            if ('FORM_TYPE' in self.registration_form
                    and self.registration_form['FORM_TYPE'].value == 'jabber:iq:register'):
                if 'username' in self.registration_form:
                    self.my_jid = JID(self.registration_form['username'].value,
                            self.my_jid.domain, self.my_jid.resource)
                if 'password' in self.registration_form:
                    self.password = self.registration_form['password'].value
            self.registration_callback = None
            self._post_connect()
        finally:
            self.lock.release()