def _digest_auth_in_stage2(self, username, _unused, stanza):
        """Handle the second stage (<iq type='set'/>) of legacy "digest"
        authentication.

        [server only]"""
        digest=stanza.xpath_eval("a:query/a:digest",{"a":"jabber:iq:auth"})
        if digest:
            digest=digest[0].getContent()
        if not digest:
            self.__logger.debug("No digest found in digest auth request")
            iq=stanza.make_error_response("bad-request")
            self.send(iq)
            return

        password,pwformat=self.get_password(username)
        if not password or pwformat!="plain":
            iq=stanza.make_error_response("bad-request")
            e=iq.get_error()
            e.add_custom_condition('jabber:iq:auth:error',"user-unauthorized")
            self.send(iq)
            return

        mydigest = hashlib.sha1(to_utf8(self.stream_id)+to_utf8(password)).hexdigest()

        if mydigest==digest:
            iq=stanza.make_result_response()
            self.send(iq)
            self.peer_authenticated=True
            self.auth_method_used="digest"
            self.state_change("authorized",self.peer)
            self._post_auth()
        else:
            self.__logger.debug("Digest auth failed: %r != %r" % (digest,mydigest))
            iq=stanza.make_error_response("bad-request")
            e=iq.get_error()
            e.add_custom_condition('jabber:iq:auth:error',"user-unauthorized")
            self.send(iq)