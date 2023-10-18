def setup(self, address, port):
        """Connects to server at `address`:`port`.

        Connects to a TCP server listening at `address`:`port` that implements
        the protocol described in the file "Generic TCP I:O Protocol.md"

        @arg address IP or address to connect to.
        @arg port port to connect to.

        @throw RuntimeError if connection was successiful but protocol isn't
               supported.
        @throw any exception thrown by `socket.socket`'s methods.
        """
        address = str(address)
        port = int(port)
        self._socket = socket.socket()
        self._socket.connect((address, port))
        self._socket.send(b'HELLO 1.0\n')
        with self._socket.makefile() as f:
            if f.readline().strip() != 'OK':
                raise RuntimeError('Protocol not supported')