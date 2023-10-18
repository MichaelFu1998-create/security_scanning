def auth_in_stage2(self,stanza):
        """Handle the second stage (<iq type='set'/>) of legacy ("plain" or
        "digest") authentication.

        [server only]"""
        self.lock.acquire()
        try:
            if "plain" not in self.auth_methods and "digest" not in self.auth_methods:
                iq=stanza.make_error_response("not-allowed")
                self.send(iq)
                return

            username=stanza.xpath_eval("a:query/a:username",{"a":"jabber:iq:auth"})
            if username:
                username=from_utf8(username[0].getContent())
            resource=stanza.xpath_eval("a:query/a:resource",{"a":"jabber:iq:auth"})
            if resource:
                resource=from_utf8(resource[0].getContent())
            if not username or not resource:
                self.__logger.debug("No username or resource found in auth request")
                iq=stanza.make_error_response("bad-request")
                self.send(iq)
                return

            if stanza.xpath_eval("a:query/a:password",{"a":"jabber:iq:auth"}):
                if "plain" not in self.auth_methods:
                    iq=stanza.make_error_response("not-allowed")
                    self.send(iq)
                    return
                else:
                    return self._plain_auth_in_stage2(username,resource,stanza)
            if stanza.xpath_eval("a:query/a:digest",{"a":"jabber:iq:auth"}):
                if "plain" not in self.auth_methods:
                    iq=stanza.make_error_response("not-allowed")
                    self.send(iq)
                    return
                else:
                    return self._digest_auth_in_stage2(username,resource,stanza)
        finally:
            self.lock.release()