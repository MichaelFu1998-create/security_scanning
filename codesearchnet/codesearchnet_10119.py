def write(self, data):
        """
        Writes data to the TLS-wrapped socket

        :param data:
            A byte string to write to the socket

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            oscrypto.errors.TLSDisconnectError - when the connection disconnects
            oscrypto.errors.TLSGracefulDisconnectError - when the remote end gracefully closed the connection
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        if self._session_context is None:
            self._raise_closed()

        processed_pointer = new(Security, 'size_t *')

        data_len = len(data)
        while data_len:
            write_buffer = buffer_from_bytes(data)
            result = Security.SSLWrite(
                self._session_context,
                write_buffer,
                data_len,
                processed_pointer
            )
            if self._exception is not None:
                exception = self._exception
                self._exception = None
                raise exception
            handle_sec_error(result, TLSError)

            bytes_written = deref(processed_pointer)
            data = data[bytes_written:]
            data_len = len(data)
            if data_len > 0:
                self.select_write()