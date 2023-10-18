def send(self, message, socket_):
        """
        Sends a message (dict) to the socket. Message consists of a 8-byte len header followed by a msgpack-numpy
            encoded dict.

        Args:
            message: The message dict (e.g. {"cmd": "reset"})
            socket_: The python socket object to use.
        """
        if not socket_:
            raise TensorForceError("No socket given in call to `send`!")
        elif not isinstance(message, dict):
            raise TensorForceError("Message to be sent must be a dict!")
        message = msgpack.packb(message)
        len_ = len(message)
        # prepend 8-byte len field to all our messages
        socket_.send(bytes("{:08d}".format(len_), encoding="ascii") + message)