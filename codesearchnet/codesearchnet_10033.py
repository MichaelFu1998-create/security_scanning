def _raw_write(self):
        """
        Takes ciphertext from the memory bio and writes it to the
        socket.

        :return:
            A byte string of ciphertext going to the socket. Used
            for debugging the handshake only.
        """

        data_available = libssl.BIO_ctrl_pending(self._wbio)
        if data_available == 0:
            return b''
        to_read = min(self._buffer_size, data_available)
        read = libssl.BIO_read(self._wbio, self._bio_write_buffer, to_read)
        to_write = bytes_from_buffer(self._bio_write_buffer, read)
        output = to_write
        while len(to_write):
            raise_disconnect = False
            try:
                sent = self._socket.send(to_write)
            except (socket_.error) as e:
                # Handle ECONNRESET and EPIPE
                if e.errno == 104 or e.errno == 32:
                    raise_disconnect = True
                else:
                    raise

            if raise_disconnect:
                raise_disconnection()
            to_write = to_write[sent:]
            if len(to_write):
                self.select_write()
        return output