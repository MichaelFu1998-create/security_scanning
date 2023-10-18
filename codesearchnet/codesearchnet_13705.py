def initiate(self, transport, to = None):
        """Initiate an XMPP connection over the `transport`.

        :Parameters:
            - `transport`: an XMPP transport instance
            - `to`: peer name (defaults to own jid domain part)
        """
        if to is None:
            to = JID(self.me.domain)
        return StreamBase.initiate(self, transport, to)