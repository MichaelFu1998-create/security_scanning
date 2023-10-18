def _advapi32_interpret_dsa_key_blob(bit_size, public_blob, private_blob):
    """
    Takes a CryptoAPI DSS private key blob and converts it into the ASN.1
    structures for the public and private keys

    :param bit_size:
        The integer bit size of the key

    :param public_blob:
        A byte string of the binary data after the public key header

    :param private_blob:
        A byte string of the binary data after the private key header

    :return:
        A 2-element tuple of (asn1crypto.keys.PublicKeyInfo,
        asn1crypto.keys.PrivateKeyInfo)
    """

    len1 = 20
    len2 = bit_size // 8

    q_offset = len2
    g_offset = q_offset + len1
    x_offset = g_offset + len2
    y_offset = x_offset

    p = int_from_bytes(private_blob[0:q_offset][::-1])
    q = int_from_bytes(private_blob[q_offset:g_offset][::-1])
    g = int_from_bytes(private_blob[g_offset:x_offset][::-1])
    x = int_from_bytes(private_blob[x_offset:x_offset + len1][::-1])
    y = int_from_bytes(public_blob[y_offset:y_offset + len2][::-1])

    public_key_info = keys.PublicKeyInfo({
        'algorithm': keys.PublicKeyAlgorithm({
            'algorithm': 'dsa',
            'parameters': keys.DSAParams({
                'p': p,
                'q': q,
                'g': g,
            })
        }),
        'public_key': core.Integer(y),
    })

    private_key_info = keys.PrivateKeyInfo({
        'version': 0,
        'private_key_algorithm': keys.PrivateKeyAlgorithm({
            'algorithm': 'dsa',
            'parameters': keys.DSAParams({
                'p': p,
                'q': q,
                'g': g,
            })
        }),
        'private_key': core.Integer(x),
    })

    return (public_key_info, private_key_info)