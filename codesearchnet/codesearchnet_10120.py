def _shutdown(self, manual):
        """
        Shuts down the TLS session and then shuts down the underlying socket

        :param manual:
            A boolean if the connection was manually shutdown
        """

        if self._session_context is None:
            return

        # Ignore error during close in case other end closed already
        result = Security.SSLClose(self._session_context)

        if osx_version_info < (10, 8):
            result = Security.SSLDisposeContext(self._session_context)
            handle_sec_error(result)
        else:
            result = CoreFoundation.CFRelease(self._session_context)
            handle_cf_error(result)

        self._session_context = None

        if manual:
            self._local_closed = True

        try:
            self._socket.shutdown(socket_.SHUT_RDWR)
        except (socket_.error):
            pass