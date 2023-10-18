def error(self,stanza):
        """
        Called when an error stanza is received.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `pyxmpp.stanza.Stanza`
        """
        err=stanza.get_error()
        self.__logger.debug("Error from: %r Condition: %r"
                % (stanza.get_from(),err.get_condition))