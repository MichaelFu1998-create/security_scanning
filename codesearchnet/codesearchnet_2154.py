def recv(self, socket_, encoding=None):
        """
        Receives a message as msgpack-numpy encoded byte-string from the given socket object.
        Blocks until something was received.

        Args:
            socket_: The python socket object to use.
            encoding (str): The encoding to use for unpacking messages from the socket.
        Returns: The decoded (as dict) message received.
        """
        unpacker = msgpack.Unpacker(encoding=encoding)

        # Wait for an immediate response.
        response = socket_.recv(8)  # get the length of the message
        if response == b"":
            raise TensorForceError("No data received by socket.recv in call to method `recv` " +
                                   "(listener possibly closed)!")
        orig_len = int(response)
        received_len = 0
        while True:
            data = socket_.recv(min(orig_len - received_len, self.max_msg_len))
            # There must be a response.
            if not data:
                raise TensorForceError("No data of len {} received by socket.recv in call to method `recv`!".
                                       format(orig_len - received_len))
            data_len = len(data)
            received_len += data_len
            unpacker.feed(data)

            if received_len == orig_len:
                break

        # Get the data.
        for message in unpacker:
            sts = message.get("status", message.get(b"status"))
            if sts:
                if sts == "ok" or sts == b"ok":
                    return message
                else:
                    raise TensorForceError("RemoteEnvironment server error: {}".
                                           format(message.get("message", "not specified")))
            else:
                raise TensorForceError("Message without field 'status' received!")
        raise TensorForceError("No message encoded in data stream (data stream had len={})".
                               format(orig_len))