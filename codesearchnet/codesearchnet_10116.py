def read(self, max_length):
        """
        Reads data from the TLS-wrapped socket

        :param max_length:
            The number of bytes to read - output may be less than this

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            oscrypto.errors.TLSDisconnectError - when the connection disconnects
            oscrypto.errors.TLSGracefulDisconnectError - when the remote end gracefully closed the connection
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library

        :return:
            A byte string of the data read
        """

        if not isinstance(max_length, int_types):
            raise TypeError(pretty_message(
                '''
                max_length must be an integer, not %s
                ''',
                type_name(max_length)
            ))

        if self._session_context is None:
            # Even if the session is closed, we can use
            # buffered data to respond to read requests
            if self._decrypted_bytes != b'':
                output = self._decrypted_bytes
                self._decrypted_bytes = b''
                return output

            self._raise_closed()

        buffered_length = len(self._decrypted_bytes)

        # If we already have enough buffered data, just use that
        if buffered_length >= max_length:
            output = self._decrypted_bytes[0:max_length]
            self._decrypted_bytes = self._decrypted_bytes[max_length:]
            return output

        # Don't block if we have buffered data available, since it is ok to
        # return less than the max_length
        if buffered_length > 0 and not self.select_read(0):
            output = self._decrypted_bytes
            self._decrypted_bytes = b''
            return output

        # Only read enough to get the requested amount when
        # combined with buffered data
        to_read = max_length - len(self._decrypted_bytes)

        read_buffer = buffer_from_bytes(to_read)
        processed_pointer = new(Security, 'size_t *')
        result = Security.SSLRead(
            self._session_context,
            read_buffer,
            to_read,
            processed_pointer
        )
        if self._exception is not None:
            exception = self._exception
            self._exception = None
            raise exception
        if result and result not in set([SecurityConst.errSSLWouldBlock, SecurityConst.errSSLClosedGraceful]):
            handle_sec_error(result, TLSError)

        if result and result == SecurityConst.errSSLClosedGraceful:
            self._gracefully_closed = True
            self._shutdown(False)
            self._raise_closed()

        bytes_read = deref(processed_pointer)
        output = self._decrypted_bytes + bytes_from_buffer(read_buffer, bytes_read)

        self._decrypted_bytes = output[max_length:]
        return output[0:max_length]