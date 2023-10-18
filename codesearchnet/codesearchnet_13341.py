def _process_handler_result(self, response):
        """Examines out the response returned by a stanza handler and sends all
        stanzas provided.

        :Parameters:
            - `response`: the response to process. `None` or `False` means 'not
              handled'. `True` means 'handled'. Stanza or stanza list means
              handled with the stanzas to send back
        :Types:
            - `response`: `bool` or `Stanza` or iterable of `Stanza`

        :Returns:
            - `True`: if `response` is `Stanza`, iterable or `True` (meaning
              the stanza was processed).
            - `False`: when `response` is `False` or `None`

        :returntype: `bool`
        """

        if response is None or response is False:
            return False

        if isinstance(response, Stanza):
            self.send(response)
            return True

        try:
            response = iter(response)
        except TypeError:
            return bool(response)

        for stanza in response:
            if isinstance(stanza, Stanza):
                self.send(stanza)
            else:
                logger.warning(u"Unexpected object in stanza handler result:"
                                                    u" {0!r}".format(stanza))
        return True