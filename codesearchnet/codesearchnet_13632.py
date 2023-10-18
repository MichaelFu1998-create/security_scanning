def _continue_tls_handshake(self):
        """Continue a TLS handshake."""
        try:
            logger.debug(" do_handshake()")
            self._socket.do_handshake()
        except ssl.SSLError, err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                self._tls_state = "want_read"
                logger.debug("   want_read")
                self._state_cond.notify()
                return
            elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                self._tls_state = "want_write"
                logger.debug("   want_write")
                self._write_queue.appendleft(TLSHandshake)
                return
            else:
                raise
        self._tls_state = "connected"
        self._set_state("connected")
        self._auth_properties['security-layer'] = "TLS"
        if "tls-unique" in CHANNEL_BINDING_TYPES:
            try:
                # pylint: disable=E1103
                tls_unique = self._socket.get_channel_binding("tls-unique")
            except ValueError:
                pass
            else:
                self._auth_properties['channel-binding'] = {
                                                    "tls-unique": tls_unique}
        try:
            cipher = self._socket.cipher()
        except AttributeError:
            # SSLSocket.cipher doesn't work on PyPy
            cipher = "unknown"
        cert = get_certificate_from_ssl_socket(self._socket)
        self.event(TLSConnectedEvent(cipher, cert))