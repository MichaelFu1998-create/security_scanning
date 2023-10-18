def _bcrypt_interpret_rsa_key_blob(key_type, blob_struct, blob):
    """
    Take a CNG BCRYPT_RSAFULLPRIVATE_BLOB and converts it into an ASN.1
    structure

    :param key_type:
        A unicode string of "private" or "public"

    :param blob_struct:
        An instance of BCRYPT_RSAKEY_BLOB

    :param blob:
        A byte string of the binary data contained after the struct

    :return:
        An asn1crypto.keys.PrivateKeyInfo or asn1crypto.keys.PublicKeyInfo
        object, based on the key_type param
    """

    public_exponent_byte_length = native(int, blob_struct.cbPublicExp)
    modulus_byte_length = native(int, blob_struct.cbModulus)

    modulus_offset = public_exponent_byte_length

    public_exponent = int_from_bytes(blob[0:modulus_offset])
    modulus = int_from_bytes(blob[modulus_offset:modulus_offset + modulus_byte_length])

    if key_type == 'public':
        return keys.PublicKeyInfo({
            'algorithm': keys.PublicKeyAlgorithm({
                'algorithm': 'rsa',
            }),
            'public_key': keys.RSAPublicKey({
                'modulus': modulus,
                'public_exponent': public_exponent,
            }),
        })

    elif key_type == 'private':
        prime1_byte_length = native(int, blob_struct.cbPrime1)
        prime2_byte_length = native(int, blob_struct.cbPrime2)

        prime1_offset = modulus_offset + modulus_byte_length
        prime2_offset = prime1_offset + prime1_byte_length
        exponent1_offset = prime2_offset + prime2_byte_length
        exponent2_offset = exponent1_offset + prime2_byte_length
        coefficient_offset = exponent2_offset + prime2_byte_length
        private_exponent_offset = coefficient_offset + prime1_byte_length

        prime1 = int_from_bytes(blob[prime1_offset:prime2_offset])
        prime2 = int_from_bytes(blob[prime2_offset:exponent1_offset])
        exponent1 = int_from_bytes(blob[exponent1_offset:exponent2_offset])
        exponent2 = int_from_bytes(blob[exponent2_offset:coefficient_offset])
        coefficient = int_from_bytes(blob[coefficient_offset:private_exponent_offset])
        private_exponent = int_from_bytes(blob[private_exponent_offset:private_exponent_offset + modulus_byte_length])

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

        return keys.PrivateKeyInfo({
            'version': 0,
            'private_key_algorithm': keys.PrivateKeyAlgorithm({
                'algorithm': 'rsa',
            }),
            'private_key': rsa_private_key,
        })

    else:
        raise ValueError(pretty_message(
            '''
            key_type must be one of "public", "private", not %s
            ''',
            repr(key_type)
        ))