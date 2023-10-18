def _abortConnection(self):
        """
        We need a way to close the connection when an event line is too long
        or if we time out waiting for an event. This is normally done by
        calling :meth:`~twisted.internet.interfaces.ITransport.loseConnection``
        or :meth:`~twisted.internet.interfaces.ITCPTransport.abortConnection`,
        but newer versions of Twisted make this complicated.

        Despite what the documentation says for
        :class:`twisted.internet.protocol.Protocol`, the ``transport``
        attribute is not necessarily a
        :class:`twisted.internet.interfaces.ITransport`. Looking at the
        documentation for :class:`twisted.internet.interfaces.IProtocol`, the
        ``transport`` attribute is actually not defined and neither is the
        type of the ``transport`` parameter to
        :meth:`~twisted.internet.interfaces.IProtocol.makeConnection`.

        ``SseProtocol`` will most often be used with HTTP requests initiated
        with :class:`twisted.web.client.Agent` which, in newer versions of
        Twisted, ends up giving us a
        :class:`twisted.web._newclient.TransportProxyProducer` for our
        ``transport``. This is just a
        :class:`twisted.internet.interfaces.IPushProducer` that wraps the
        actual transport. If our transport is one of these, try call
        ``abortConnection()`` on the underlying transport.
        """
        transport = self.transport
        if isinstance(transport, TransportProxyProducer):
            transport = transport._producer

        if hasattr(transport, 'abortConnection'):
            transport.abortConnection()
        else:
            self.log.error(
                'Transport {} has no abortConnection method'.format(transport))