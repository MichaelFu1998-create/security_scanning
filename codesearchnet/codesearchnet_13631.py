def _initiate_starttls(self, **kwargs):
        """Initiate starttls handshake over the socket.
        """
        if self._tls_state == "connected":
            raise RuntimeError("Already TLS-connected")
        kwargs["do_handshake_on_connect"] = False
        logger.debug("Wrapping the socket into ssl")
        self._socket = ssl.wrap_socket(self._socket, **kwargs)
        self._set_state("tls-handshake")
        self._continue_tls_handshake()