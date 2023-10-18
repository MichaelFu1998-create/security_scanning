def from_string(cls, key_pem, is_x509_cert):
        """Construct an RsaVerifier instance from a string.

        Args:
            key_pem: string, public key in PEM format.
            is_x509_cert: bool, True if key_pem is an X509 cert, otherwise it
                          is expected to be an RSA key in PEM format.

        Returns:
            RsaVerifier instance.

        Raises:
            ValueError: if the key_pem can't be parsed. In either case, error
                        will begin with 'No PEM start marker'. If
                        ``is_x509_cert`` is True, will fail to find the
                        "-----BEGIN CERTIFICATE-----" error, otherwise fails
                        to find "-----BEGIN RSA PUBLIC KEY-----".
        """
        key_pem = _helpers._to_bytes(key_pem)
        if is_x509_cert:
            der = rsa.pem.load_pem(key_pem, 'CERTIFICATE')
            asn1_cert, remaining = decoder.decode(der, asn1Spec=Certificate())
            if remaining != b'':
                raise ValueError('Unused bytes', remaining)

            cert_info = asn1_cert['tbsCertificate']['subjectPublicKeyInfo']
            key_bytes = _bit_list_to_bytes(cert_info['subjectPublicKey'])
            pubkey = rsa.PublicKey.load_pkcs1(key_bytes, 'DER')
        else:
            pubkey = rsa.PublicKey.load_pkcs1(key_pem, 'PEM')
        return cls(pubkey)