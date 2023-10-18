def _request_tls(self):
        """Request a TLS-encrypted connection.

        [initiating entity only]"""
        self.requested = True
        element = ElementTree.Element(STARTTLS_TAG)
        self.stream.write_element(element)