def from_string(key_pem, is_x509_cert):
        """Construct a Verified instance from a string.

        Args:
            key_pem: string, public key in PEM format.
            is_x509_cert: bool, True if key_pem is an X509 cert, otherwise it
                          is expected to be an RSA key in PEM format.

        Returns:
            Verifier instance.
        """
        if is_x509_cert:
            key_pem = _helpers._to_bytes(key_pem)
            pemLines = key_pem.replace(b' ', b'').split()
            certDer = _helpers._urlsafe_b64decode(b''.join(pemLines[1:-1]))
            certSeq = DerSequence()
            certSeq.decode(certDer)
            tbsSeq = DerSequence()
            tbsSeq.decode(certSeq[0])
            pubkey = RSA.importKey(tbsSeq[6])
        else:
            pubkey = RSA.importKey(key_pem)
        return PyCryptoVerifier(pubkey)