def intermediates(self):
        """
        A list of asn1crypto.x509.Certificate objects that were presented as
        intermediates by the server
        """

        if self._context_handle_pointer is None:
            self._raise_closed()

        if self._certificate is None:
            self._read_certificates()

        return self._intermediates