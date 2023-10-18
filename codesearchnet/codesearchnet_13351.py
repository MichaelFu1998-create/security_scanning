def _set_response_handlers(self, stanza, res_handler, err_handler,
                                timeout_handler = None, timeout = None):
        """Same as `set_response_handlers` but assume `self.lock` is
        acquired."""
        # pylint: disable-msg=R0913
        self.fix_out_stanza(stanza)
        to_jid = stanza.to_jid
        if to_jid:
            to_jid = unicode(to_jid)
        if timeout_handler:
            def callback(dummy1, dummy2):
                """Wrapper for the timeout handler to make it compatible
                with the `ExpiringDictionary` """
                timeout_handler()
            self._iq_response_handlers.set_item(
                                    (stanza.stanza_id, to_jid),
                                    (res_handler,err_handler),
                                    timeout, callback)
        else:
            self._iq_response_handlers.set_item(
                                    (stanza.stanza_id, to_jid),
                                    (res_handler, err_handler),
                                    timeout)