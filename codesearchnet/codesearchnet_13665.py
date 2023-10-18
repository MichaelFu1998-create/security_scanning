def _auth_stage1(self):
        """Do the first stage (<iq type='get'/>) of legacy ("plain" or
        "digest") authentication.

        [client only]"""
        iq=Iq(stanza_type="get")
        q=iq.new_query("jabber:iq:auth")
        q.newTextChild(None,"username",to_utf8(self.my_jid.node))
        q.newTextChild(None,"resource",to_utf8(self.my_jid.resource))
        self.send(iq)
        self.set_response_handlers(iq,self.auth_stage2,self.auth_error,
                            self.auth_timeout,timeout=60)
        iq.free()