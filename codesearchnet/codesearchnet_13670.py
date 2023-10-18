def _plain_auth_in_stage2(self, username, _unused, stanza):
        """Handle the second stage (<iq type='set'/>) of legacy "plain"
        authentication.

        [server only]"""
        password=stanza.xpath_eval("a:query/a:password",{"a":"jabber:iq:auth"})
        if password:
            password=from_utf8(password[0].getContent())
        if not password:
            self.__logger.debug("No password found in plain auth request")
            iq=stanza.make_error_response("bad-request")
            self.send(iq)
            return

        if self.check_password(username,password):
            iq=stanza.make_result_response()
            self.send(iq)
            self.peer_authenticated=True
            self.auth_method_used="plain"
            self.state_change("authorized",self.peer)
            self._post_auth()
        else:
            self.__logger.debug("Plain auth failed")
            iq=stanza.make_error_response("bad-request")
            e=iq.get_error()
            e.add_custom_condition('jabber:iq:auth:error',"user-unauthorized")
            self.send(iq)