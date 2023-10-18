def _unarmor_pem(data, password=None):
    """
    Removes PEM-encoding from a public key, private key or certificate. If the
    private key is encrypted, the password will be used to decrypt it.

    :param data:
        A byte string of the PEM-encoded data

    :param password:
        A byte string of the encryption password, or None

    :return:
        A 3-element tuple in the format: (key_type, algorithm, der_bytes). The
        key_type will be a unicode string of "public key", "private key" or
        "certificate". The algorithm will be a unicode string of "rsa", "dsa"
        or "ec".
    """

    object_type, headers, der_bytes = pem.unarmor(data)

    type_regex = '^((DSA|EC|RSA) PRIVATE KEY|ENCRYPTED PRIVATE KEY|PRIVATE KEY|PUBLIC KEY|RSA PUBLIC KEY|CERTIFICATE)'
    armor_type = re.match(type_regex, object_type)
    if not armor_type:
        raise ValueError(pretty_message(
            '''
            data does not seem to contain a PEM-encoded certificate, private
            key or public key
            '''
        ))

    pem_header = armor_type.group(1)

    data = data.strip()

    # RSA private keys are encrypted after being DER-encoded, but before base64
    # encoding, so they need to be hanlded specially
    if pem_header in set(['RSA PRIVATE KEY', 'DSA PRIVATE KEY', 'EC PRIVATE KEY']):
        algo = armor_type.group(2).lower()
        return ('private key', algo, _unarmor_pem_openssl_private(headers, der_bytes, password))

    key_type = pem_header.lower()
    algo = None
    if key_type == 'encrypted private key':
        key_type = 'private key'
    elif key_type == 'rsa public key':
        key_type = 'public key'
        algo = 'rsa'

    return (key_type, algo, der_bytes)