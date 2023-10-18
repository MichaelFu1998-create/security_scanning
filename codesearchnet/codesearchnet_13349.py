def process_stanza(self, stanza):
        """Process stanza received from the stream.

        First "fix" the stanza with `self.fix_in_stanza()`,
        then pass it to `self.route_stanza()` if it is not directed
        to `self.me` and `self.process_all_stanzas` is not True. Otherwise
        stanza is passwd to `self.process_iq()`, `self.process_message()`
        or `self.process_presence()` appropriately.

        :Parameters:
            - `stanza`: the stanza received.

        :returns: `True` when stanza was handled
        """

        self.fix_in_stanza(stanza)
        to_jid = stanza.to_jid

        if not self.process_all_stanzas and to_jid and (
                to_jid != self.me and to_jid.bare() != self.me.bare()):
            return self.route_stanza(stanza)

        try:
            if isinstance(stanza, Iq):
                if self.process_iq(stanza):
                    return True
            elif isinstance(stanza, Message):
                if self.process_message(stanza):
                    return True
            elif isinstance(stanza, Presence):
                if self.process_presence(stanza):
                    return True
        except ProtocolError, err:
            typ = stanza.stanza_type
            if typ != 'error' and (typ != 'result'
                                                or stanza.stanza_type != 'iq'):
                response = stanza.make_error_response(err.xmpp_name)
                self.send(response)
                err.log_reported()
            else:
                err.log_ignored()
            return
        logger.debug("Unhandled %r stanza: %r" % (stanza.stanza_type,
                                                        stanza.serialize()))
        return False