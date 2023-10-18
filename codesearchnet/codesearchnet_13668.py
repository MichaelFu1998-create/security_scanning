def auth_stage2(self,stanza):
        """Handle the first stage authentication response (result of the <iq
        type="get"/>).

        [client only]"""
        self.lock.acquire()
        try:
            self.__logger.debug("Procesing auth response...")
            self.available_auth_methods=[]
            if (stanza.xpath_eval("a:query/a:digest",{"a":"jabber:iq:auth"}) and self.stream_id):
                self.available_auth_methods.append("digest")
            if (stanza.xpath_eval("a:query/a:password",{"a":"jabber:iq:auth"})):
                self.available_auth_methods.append("plain")
            self.auth_stanza=stanza.copy()
            self._try_auth()
        finally:
            self.lock.release()