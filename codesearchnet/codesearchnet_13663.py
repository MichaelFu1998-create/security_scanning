def auth_in_stage1(self,stanza):
        """Handle the first stage (<iq type='get'/>) of legacy ("plain" or
        "digest") authentication.

        [server only]"""
        self.lock.acquire()
        try:
            if "plain" not in self.auth_methods and "digest" not in self.auth_methods:
                iq=stanza.make_error_response("not-allowed")
                self.send(iq)
                return

            iq=stanza.make_result_response()
            q=iq.new_query("jabber:iq:auth")
            q.newChild(None,"username",None)
            q.newChild(None,"resource",None)
            if "plain" in self.auth_methods:
                q.newChild(None,"password",None)
            if "digest" in self.auth_methods:
                q.newChild(None,"digest",None)
            self.send(iq)
            iq.free()
        finally:
            self.lock.release()