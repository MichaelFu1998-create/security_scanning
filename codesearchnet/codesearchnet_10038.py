def certificate(self):
        """
        An asn1crypto.x509.Certificate object of the end-entity certificate
        presented by the server
        """

        if self._ssl is None:
            self._raise_closed()

        if self._certificate is None:
            self._read_certificates()

        return self._certificate