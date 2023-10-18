def from_string(key, password='notasecret'):
        """Construct a Signer instance from a string.

        Args:
            key: string, private key in PEM format.
            password: string, password for private key file. Unused for PEM
                      files.

        Returns:
            Signer instance.

        Raises:
            NotImplementedError if the key isn't in PEM format.
        """
        parsed_pem_key = _helpers._parse_pem_key(_helpers._to_bytes(key))
        if parsed_pem_key:
            pkey = RSA.importKey(parsed_pem_key)
        else:
            raise NotImplementedError(
                'No key in PEM format was detected. This implementation '
                'can only use the PyCrypto library for keys in PEM '
                'format.')
        return PyCryptoSigner(pkey)