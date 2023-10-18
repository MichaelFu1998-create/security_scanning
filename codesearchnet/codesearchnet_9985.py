def _advapi32_interpret_rsa_key_blob(bit_size, blob_struct, blob):
    """
    Takes a CryptoAPI RSA private key blob and converts it into the ASN.1
    structures for the public and private keys

    :param bit_size:
        The integer bit size of the key

    :param blob_struct:
        An instance of the advapi32.RSAPUBKEY struct

    :param blob:
        A byte string of the binary data after the header

    :return:
        A 2-element tuple of (asn1crypto.keys.PublicKeyInfo,
        asn1crypto.keys.PrivateKeyInfo)
    """

    len1 = bit_size // 8
    len2 = bit_size // 16

    prime1_offset = len1
    prime2_offset = prime1_offset + len2
    exponent1_offset = prime2_offset + len2
    exponent2_offset = exponent1_offset + len2
    coefficient_offset = exponent2_offset + len2
    private_exponent_offset = coefficient_offset + len2

    public_exponent = blob_struct.rsapubkey.pubexp
    modulus = int_from_bytes(blob[0:prime1_offset][::-1])
    prime1 = int_from_bytes(blob[prime1_offset:prime2_offset][::-1])
    prime2 = int_from_bytes(blob[prime2_offset:exponent1_offset][::-1])
    exponent1 = int_from_bytes(blob[exponent1_offset:exponent2_offset][::-1])
    exponent2 = int_from_bytes(blob[exponent2_offset:coefficient_offset][::-1])
    coefficient = int_from_bytes(blob[coefficient_offset:private_exponent_offset][::-1])
    private_exponent = int_from_bytes(blob[private_exponent_offset:private_exponent_offset + len1][::-1])

    public_key_info = keys.PublicKeyInfo({
        'algorithm': keys.PublicKeyAlgorithm({
            'algorithm': 'rsa',
        }),
        'public_key': keys.RSAPublicKey({
            'modulus': modulus,
            'public_exponent': public_exponent,
        }),
    })

    rsa_private_key = keys.RSAPrivateKey({
        'version': 'two-prime',
        'modulus': modulus,
        'public_exponent': public_exponent,
        'private_exponent': private_exponent,
        'prime1': prime1,
        'prime2': prime2,
        'exponent1': exponent1,
        'exponent2': exponent2,
        'coefficient': coefficient,
    })

    private_key_info = keys.PrivateKeyInfo({
        'version': 0,
        'private_key_algorithm': keys.PrivateKeyAlgorithm({
            'algorithm': 'rsa',
        }),
        'private_key': rsa_private_key,
    })

    return (public_key_info, private_key_info)