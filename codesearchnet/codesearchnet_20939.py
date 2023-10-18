def stop(self):
        """ Stop streaming """

        if self._protocol:
            self._protocol.factory.continueTrying = 0
            self._protocol.transport.loseConnection()

        if self._reactor and self._reactor.running:
            self._reactor.stop()