def request_configuration_form(self):
        """
        Request a configuration form for the room.

        When the form is received `self.handler.configuration_form_received` will be called.
        When an error response is received then `self.handler.error` will be called.

        :return: id of the request stanza.
        :returntype: `unicode`
        """
        iq = Iq(to_jid = self.room_jid.bare(), stanza_type = "get")
        iq.new_query(MUC_OWNER_NS, "query")
        self.manager.stream.set_response_handlers(
                iq, self.process_configuration_form_success, self.process_configuration_form_error)
        self.manager.stream.send(iq)
        return iq.get_id()