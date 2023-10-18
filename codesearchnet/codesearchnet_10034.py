def read(self, max_length):
        """
        Reads data from the TLS-wrapped socket

        :param max_length:
            The number of bytes to read - output may be less than this

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
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

        buffered_length = len(self._decrypted_bytes)

        # If we already have enough buffered data, just use that
        if buffered_length >= max_length:
            output = self._decrypted_bytes[0:max_length]
            self._decrypted_bytes = self._decrypted_bytes[max_length:]
            return output

        if self._ssl is None:
            self._raise_closed()

        # Don't block if we have buffered data available, since it is ok to
        # return less than the max_length
        if buffered_length > 0 and not self.select_read(0):
            output = self._decrypted_bytes
            self._decrypted_bytes = b''
            return output

        # Only read enough to get the requested amount when
        # combined with buffered data
        to_read = min(self._buffer_size, max_length - buffered_length)

        output = self._decrypted_bytes

        # The SSL_read() loop handles renegotiations, so we need to handle
        # requests for both reads and writes
        again = True
        while again:
            again = False
            result = libssl.SSL_read(self._ssl, self._read_buffer, to_read)
            self._raw_write()
            if result <= 0:

                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    if self._raw_read() != b'':
                        again = True
                        continue
                    raise_disconnection()

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write()
                    again = True
                    continue

                elif error == LibsslConst.SSL_ERROR_ZERO_RETURN:
                    self._gracefully_closed = True
                    self._shutdown(False)
                    break

                else:
                    handle_openssl_error(0, TLSError)

            output += bytes_from_buffer(self._read_buffer, result)

        if self._gracefully_closed and len(output) == 0:
            self._raise_closed()

        self._decrypted_bytes = output[max_length:]
        return output[0:max_length]