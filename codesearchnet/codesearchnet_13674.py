def registration_error(self, stanza):
        """Handle in-band registration error.

        [client only]

        :Parameters:
            - `stanza`: the error stanza received or `None` on timeout.
        :Types:
            - `stanza`: `pyxmpp.stanza.Stanza`"""
        self.lock.acquire()
        try:
            err=stanza.get_error()
            ae=err.xpath_eval("e:*",{"e":"jabber:iq:auth:error"})
            if ae:
                ae=ae[0].name
            else:
                ae=err.get_condition().name
            raise RegistrationError("Authentication error condition: %s" % (ae,))
        finally:
            self.lock.release()