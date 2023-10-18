def from_string(key_pem, is_x509_cert):
        """Construct a Verified instance from a string.

        Args:
            key_pem: string, public key in PEM format.
            is_x509_cert: bool, True if key_pem is an X509 cert, otherwise it
                          is expected to be an RSA key in PEM format.

        Returns:
            Verifier instance.

        Raises:
            OpenSSL.crypto.Error: if the key_pem can't be parsed.
        """
        key_pem = _helpers._to_bytes(key_pem)
        if is_x509_cert:
            pubkey = crypto.load_certificate(crypto.FILETYPE_PEM, key_pem)
        else:
            pubkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_pem)
        return OpenSSLVerifier(pubkey)