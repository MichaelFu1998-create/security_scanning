def dump_public_key(public_key, encoding='pem'):
    """
    Serializes a public key object into a byte string

    :param public_key:
        An oscrypto.asymmetric.PublicKey or asn1crypto.keys.PublicKeyInfo object

    :param encoding:
        A unicode string of "pem" or "der"

    :return:
        A byte string of the encoded public key
    """

    if encoding not in set(['pem', 'der']):
        raise ValueError(pretty_message(
            '''
            encoding must be one of "pem", "der", not %s
            ''',
            repr(encoding)
        ))

    is_oscrypto = isinstance(public_key, PublicKey)
    if not isinstance(public_key, keys.PublicKeyInfo) and not is_oscrypto:
        raise TypeError(pretty_message(
            '''
            public_key must be an instance of oscrypto.asymmetric.PublicKey or
            asn1crypto.keys.PublicKeyInfo, not %s
            ''',
            type_name(public_key)
        ))

    if is_oscrypto:
        public_key = public_key.asn1

    output = public_key.dump()
    if encoding == 'pem':
        output = pem.armor('PUBLIC KEY', output)
    return output