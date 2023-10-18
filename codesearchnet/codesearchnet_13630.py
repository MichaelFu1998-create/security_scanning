def getpeercert(self):
        """Return the peer certificate.

        :ReturnType: `pyxmpp2.cert.Certificate`
        """
        with self.lock:
            if not self._socket or self._tls_state != "connected":
                raise ValueError("Not TLS-connected")
            return get_certificate_from_ssl_socket(self._socket)