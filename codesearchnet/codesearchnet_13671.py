def _digest_auth_stage2(self, _unused):
        """Do the second stage (<iq type='set'/>) of legacy "digest"
        authentication.

        [client only]"""
        iq=Iq(stanza_type="set")
        q=iq.new_query("jabber:iq:auth")
        q.newTextChild(None,"username",to_utf8(self.my_jid.node))
        q.newTextChild(None,"resource",to_utf8(self.my_jid.resource))

        digest = hashlib.sha1(to_utf8(self.stream_id)+to_utf8(self.password)).hexdigest()

        q.newTextChild(None,"digest",digest)
        self.send(iq)
        self.set_response_handlers(iq,self.auth_finish,self.auth_error)
        iq.free()