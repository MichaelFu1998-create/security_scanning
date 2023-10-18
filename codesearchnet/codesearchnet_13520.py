def _make_tls_connection(self):
        """Initiate TLS connection.

        [initiating entity only]
        """
        logger.debug("Preparing TLS connection")
        if self.settings["tls_verify_peer"]:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE
        self.stream.transport.starttls(
                    keyfile = self.settings["tls_key_file"],
                    certfile = self.settings["tls_cert_file"],
                    server_side = not self.stream.initiator,
                    cert_reqs = cert_reqs,
                    ssl_version = ssl.PROTOCOL_TLSv1,
                    ca_certs = self.settings["tls_cacert_file"],
                    do_handshake_on_connect = False,
                    )