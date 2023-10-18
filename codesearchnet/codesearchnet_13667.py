def auth_error(self,stanza):
        """Handle legacy authentication error.

        [client only]"""
        self.lock.acquire()
        try:
            err=stanza.get_error()
            ae=err.xpath_eval("e:*",{"e":"jabber:iq:auth:error"})
            if ae:
                ae=ae[0].name
            else:
                ae=err.get_condition().name
            raise LegacyAuthenticationError("Authentication error condition: %s"
                        % (ae,))
        finally:
            self.lock.release()