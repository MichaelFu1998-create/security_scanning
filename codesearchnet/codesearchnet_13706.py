def receive(self, transport, myname = None):
        """Receive an XMPP connection over the `transport`.

        :Parameters:
            - `transport`: an XMPP transport instance
            - `myname`: local stream endpoint name (defaults to own jid domain
              part).
        """
        if myname is None:
            myname = JID(self.me.domain)
        return StreamBase.receive(self, transport, myname)