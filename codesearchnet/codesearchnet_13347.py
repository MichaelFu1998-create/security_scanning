def process_presence(self, stanza):
        """Process presence stanza.

        Pass it to a handler of the stanza's type and payload namespace.

        :Parameters:
            - `stanza`: presence stanza to be handled
        """

        stanza_type = stanza.stanza_type
        return self.__try_handlers(self._presence_handlers, stanza, stanza_type)