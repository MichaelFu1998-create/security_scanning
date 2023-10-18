def from_string(cls, key, password='notasecret'):
        """Construct an RsaSigner instance from a string.

        Args:
            key: string, private key in PEM format.
            password: string, password for private key file. Unused for PEM
                      files.

        Returns:
            RsaSigner instance.

        Raises:
            ValueError if the key cannot be parsed as PKCS#1 or PKCS#8 in
            PEM format.
        """
        key = _helpers._from_bytes(key)  # pem expects str in Py3
        marker_id, key_bytes = pem.readPemBlocksFromFile(
            six.StringIO(key), _PKCS1_MARKER, _PKCS8_MARKER)

        if marker_id == 0:
            pkey = rsa.key.PrivateKey.load_pkcs1(key_bytes,
                                                 format='DER')
        elif marker_id == 1:
            key_info, remaining = decoder.decode(
                key_bytes, asn1Spec=_PKCS8_SPEC)
            if remaining != b'':
                raise ValueError('Unused bytes', remaining)
            pkey_info = key_info.getComponentByName('privateKey')
            pkey = rsa.key.PrivateKey.load_pkcs1(pkey_info.asOctets(),
                                                 format='DER')
        else:
            raise ValueError('No key could be detected.')

        return cls(pkey)