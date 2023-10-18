def _process_iq_response(self, stanza):
        """Process IQ stanza of type 'response' or 'error'.

        :Parameters:
            - `stanza`: the stanza received
        :Types:
            - `stanza`: `Iq`

        If a matching handler is available pass the stanza to it.  Otherwise
        ignore it if it is "error" or "result" stanza or return
        "feature-not-implemented" error if it is "get" or "set".
        """
        stanza_id = stanza.stanza_id
        from_jid = stanza.from_jid
        if from_jid:
            ufrom = from_jid.as_unicode()
        else:
            ufrom = None
        res_handler = err_handler = None
        try:
            res_handler, err_handler = self._iq_response_handlers.pop(
                                                    (stanza_id, ufrom))
        except KeyError:
            logger.debug("No response handler for id={0!r} from={1!r}"
                                                .format(stanza_id, ufrom))
            logger.debug(" from_jid: {0!r} peer: {1!r}  me: {2!r}"
                                        .format(from_jid, self.peer, self.me))
            if ( (from_jid == self.peer or from_jid == self.me
                            or self.me and from_jid == self.me.bare()) ):
                try:
                    logger.debug("  trying id={0!r} from=None"
                                                        .format(stanza_id))
                    res_handler, err_handler = \
                            self._iq_response_handlers.pop(
                                                    (stanza_id, None))
                except KeyError:
                    pass
        if stanza.stanza_type == "result":
            if res_handler:
                response = res_handler(stanza)
            else:
                return False
        else:
            if err_handler:
                response = err_handler(stanza)
            else:
                return False
        self._process_handler_result(response)
        return True