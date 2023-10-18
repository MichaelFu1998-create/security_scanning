def process_configuration_form_success(self, stanza):
        """
        Process successful result of a room configuration form request.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `Presence`
        """
        if stanza.get_query_ns() != MUC_OWNER_NS:
            raise ValueError("Bad result namespace") # TODO: ProtocolError
        query = stanza.get_query()
        form = None
        for el in xml_element_ns_iter(query.children, DATAFORM_NS):
            form = Form(el)
            break
        if not form:
            raise ValueError("No form received") # TODO: ProtocolError
        self.configuration_form = form
        self.handler.configuration_form_received(form)