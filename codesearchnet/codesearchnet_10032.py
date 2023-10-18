def _raw_read(self):
        """
        Reads data from the socket and writes it to the memory bio
        used by libssl to decrypt the data. Returns the unencrypted
        data for the purpose of debugging handshakes.

        :return:
            A byte string of ciphertext from the socket. Used for
            debugging the handshake only.
        """

        data = self._raw_bytes
        try:
            data += self._socket.recv(8192)
        except (socket_.error):
            pass
        output = data
        written = libssl.BIO_write(self._rbio, data, len(data))
        self._raw_bytes = data[written:]
        return output