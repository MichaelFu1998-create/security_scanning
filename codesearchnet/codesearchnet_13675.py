def registration_form_received(self, stanza):
        """Handle registration form received.

        [client only]

        Call self.registration_callback with the registration form received
        as the argument. Use the value returned by the callback will be a
        filled-in form.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `pyxmpp.iq.Iq`"""
        self.lock.acquire()
        try:
            self.__register = Register(stanza.get_query())
            self.registration_callback(stanza, self.__register.get_form())
        finally:
            self.lock.release()