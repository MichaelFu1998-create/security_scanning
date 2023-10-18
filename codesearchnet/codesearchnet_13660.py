def _post_connect(self):
        """Initialize authentication when the connection is established
        and we are the initiator."""
        if not self.initiator:
            if "plain" in self.auth_methods or "digest" in self.auth_methods:
                self.set_iq_get_handler("query","jabber:iq:auth",
                            self.auth_in_stage1)
                self.set_iq_set_handler("query","jabber:iq:auth",
                            self.auth_in_stage2)
        elif self.registration_callback:
            iq = Iq(stanza_type = "get")
            iq.set_content(Register())
            self.set_response_handlers(iq, self.registration_form_received, self.registration_error)
            self.send(iq)
            return
        ClientStream._post_connect(self)