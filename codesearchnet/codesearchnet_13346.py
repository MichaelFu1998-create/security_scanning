def process_message(self, stanza):
        """Process message stanza.

        Pass it to a handler of the stanza's type and payload namespace.
        If no handler for the actual stanza type succeeds then hadlers
        for type "normal" are used.

        :Parameters:
            - `stanza`: message stanza to be handled
        """

        stanza_type = stanza.stanza_type
        if stanza_type is None:
            stanza_type = "normal"

        if self.__try_handlers(self._message_handlers, stanza,
                                                stanza_type = stanza_type):
            return True

        if stanza_type not in ("error", "normal"):
            # try 'normal' handler additionaly to the regular handler
            return self.__try_handlers(self._message_handlers, stanza,
                                                    stanza_type = "normal")
        return False