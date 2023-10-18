def _shutdown(self, manual):
        """
        Shuts down the TLS session and then shuts down the underlying socket

        :param manual:
            A boolean if the connection was manually shutdown
        """

        if self._ssl is None:
            return

        while True:
            result = libssl.SSL_shutdown(self._ssl)

            # Don't be noisy if the socket is already closed
            try:
                self._raw_write()
            except (TLSDisconnectError):
                pass

            if result >= 0:
                break
            if result < 0:
                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    if self._raw_read() != b'':
                        continue
                    else:
                        break

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write()
                    continue

                else:
                    handle_openssl_error(0, TLSError)

        if manual:
            self._local_closed = True

        libssl.SSL_free(self._ssl)
        self._ssl = None
        # BIOs are freed by SSL_free()
        self._rbio = None
        self._wbio = None

        try:
            self._socket.shutdown(socket_.SHUT_RDWR)
        except (socket_.error):
            pass