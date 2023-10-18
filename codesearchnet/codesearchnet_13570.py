def configure_room(self, form):
        """
        Configure the room using the provided data.
        Do nothing if the provided form is of type 'cancel'.

        :Parameters:
            - `form`: the configuration parameters. Should be a 'submit' form made by filling-in
              the configuration form retireved using `self.request_configuration_form` or
              a 'cancel' form.
        :Types:
            - `form`: `Form`

        :return: id of the request stanza or `None` if a 'cancel' form was provieded.
        :returntype: `unicode`
        """

        if form.type == "cancel":
            return None
        elif form.type != "submit":
            raise ValueError("A 'submit' form required to configure a room")
        iq = Iq(to_jid = self.room_jid.bare(), stanza_type = "set")
        query = iq.new_query(MUC_OWNER_NS, "query")
        form.as_xml(query)
        self.manager.stream.set_response_handlers(
                iq, self.process_configuration_success, self.process_configuration_error)
        self.manager.stream.send(iq)
        return iq.get_id()