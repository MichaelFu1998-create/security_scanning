def write(self, data):
        """
        Writes data to the TLS-wrapped socket

        :param data:
            A byte string to write to the socket

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        data_len = len(data)
        while data_len:
            if self._ssl is None:
                self._raise_closed()
            result = libssl.SSL_write(self._ssl, data, data_len)
            self._raw_write()
            if result <= 0:

                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    if self._raw_read() != b'':
                        continue
                    raise_disconnection()

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write()
                    continue

                elif error == LibsslConst.SSL_ERROR_ZERO_RETURN:
                    self._gracefully_closed = True
                    self._shutdown(False)
                    self._raise_closed()

                else:
                    handle_openssl_error(0, TLSError)

            data = data[result:]
            data_len = len(data)