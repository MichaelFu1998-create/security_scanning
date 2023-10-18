def fetch(self):
        """Initialize the Service Discovery process."""
        from ..iq import Iq
        jid,node = self.address
        iq = Iq(to_jid = jid, stanza_type = "get")
        disco = self.disco_class(node)
        iq.add_content(disco.xmlnode)
        self.stream.set_response_handlers(iq,self.__response, self.__error,
                self.__timeout)
        self.stream.send(iq)