def run(self):
        """ Called by the process, it runs it.

        NEVER call this method directly. Instead call start() to start the separate process.
        If you don't want to use a second process, then call fetch() directly on this istance.

        To stop, call terminate()
        """
        if not self._queue:
            raise Exception("No queue available to send messages")

        factory = LiveStreamFactory(self)
        self._reactor.connectSSL("streaming.campfirenow.com", 443, factory, ssl.ClientContextFactory())
        self._reactor.run()