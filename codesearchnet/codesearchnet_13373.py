def base_handlers_factory(self):
        """Default base client handlers factory.

        Subclasses can provide different behaviour by overriding this.

        :Return: list of handlers
        """
        tls_handler = StreamTLSHandler(self.settings)
        sasl_handler = StreamSASLHandler(self.settings)
        session_handler = SessionHandler()
        binding_handler = ResourceBindingHandler(self.settings)
        return [tls_handler, sasl_handler, binding_handler, session_handler]