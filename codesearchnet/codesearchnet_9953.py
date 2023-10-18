def _parse_safe_contents(safe_contents, certs, private_keys, password):
    """
    Parses a SafeContents PKCS#12 ANS.1 structure and extracts certs and keys

    :param safe_contents:
        A byte string of ber-encoded SafeContents, or a asn1crypto.pkcs12.SafeContents
        parsed object

    :param certs:
        A dict to store certificates in

    :param keys:
        A dict to store keys in

    :param password:
        A byte string of the password to any encrypted data
    """

    if isinstance(safe_contents, byte_cls):
        safe_contents = pkcs12.SafeContents.load(safe_contents)

    for safe_bag in safe_contents:
        bag_value = safe_bag['bag_value']

        if isinstance(bag_value, pkcs12.CertBag):
            if bag_value['cert_id'].native == 'x509':
                cert = bag_value['cert_value'].parsed
                public_key_info = cert['tbs_certificate']['subject_public_key_info']
                certs[public_key_info.fingerprint] = bag_value['cert_value'].parsed

        elif isinstance(bag_value, keys.PrivateKeyInfo):
            private_keys[bag_value.fingerprint] = bag_value

        elif isinstance(bag_value, keys.EncryptedPrivateKeyInfo):
            encryption_algorithm_info = bag_value['encryption_algorithm']
            encrypted_key_bytes = bag_value['encrypted_data'].native
            decrypted_key_bytes = _decrypt_encrypted_data(encryption_algorithm_info, encrypted_key_bytes, password)
            private_key = keys.PrivateKeyInfo.load(decrypted_key_bytes)
            private_keys[private_key.fingerprint] = private_key

        elif isinstance(bag_value, pkcs12.SafeContents):
            _parse_safe_contents(bag_value, certs, private_keys, password)

        else:
            # We don't care about CRL bags or secret bags
            pass