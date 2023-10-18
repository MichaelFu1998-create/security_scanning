def _bcrypt_interpret_dsa_key_blob(key_type, version, blob_struct, blob):
    """
    Take a CNG BCRYPT_DSA_KEY_BLOB or BCRYPT_DSA_KEY_BLOB_V2 and converts it
    into an ASN.1 structure

    :param key_type:
        A unicode string of "private" or "public"

    :param version:
        An integer - 1 or 2, indicating the blob is BCRYPT_DSA_KEY_BLOB or
        BCRYPT_DSA_KEY_BLOB_V2

    :param blob_struct:
        An instance of BCRYPT_DSA_KEY_BLOB or BCRYPT_DSA_KEY_BLOB_V2

    :param blob:
        A byte string of the binary data contained after the struct

    :return:
        An asn1crypto.keys.PrivateKeyInfo or asn1crypto.keys.PublicKeyInfo
        object, based on the key_type param
    """

    key_byte_length = native(int, blob_struct.cbKey)

    if version == 1:
        q = int_from_bytes(native(byte_cls, blob_struct.q))

        g_offset = key_byte_length
        public_offset = g_offset + key_byte_length
        private_offset = public_offset + key_byte_length

        p = int_from_bytes(blob[0:g_offset])
        g = int_from_bytes(blob[g_offset:public_offset])

    elif version == 2:
        seed_byte_length = native(int, blob_struct.cbSeedLength)
        group_byte_length = native(int, blob_struct.cbGroupSize)

        q_offset = seed_byte_length
        p_offset = q_offset + group_byte_length
        g_offset = p_offset + key_byte_length
        public_offset = g_offset + key_byte_length
        private_offset = public_offset + key_byte_length

        # The seed is skipped since it is not part of the ASN.1 structure
        q = int_from_bytes(blob[q_offset:p_offset])
        p = int_from_bytes(blob[p_offset:g_offset])
        g = int_from_bytes(blob[g_offset:public_offset])

    else:
        raise ValueError('version must be 1 or 2, not %s' % repr(version))

    if key_type == 'public':
        public = int_from_bytes(blob[public_offset:private_offset])
        return keys.PublicKeyInfo({
            'algorithm': keys.PublicKeyAlgorithm({
                'algorithm': 'dsa',
                'parameters': keys.DSAParams({
                    'p': p,
                    'q': q,
                    'g': g,
                })
            }),
            'public_key': core.Integer(public),
        })

    elif key_type == 'private':
        private = int_from_bytes(blob[private_offset:private_offset + key_byte_length])
        return keys.PrivateKeyInfo({
            'version': 0,
            'private_key_algorithm': keys.PrivateKeyAlgorithm({
                'algorithm': 'dsa',
                'parameters': keys.DSAParams({
                    'p': p,
                    'q': q,
                    'g': g,
                })
            }),
            'private_key': core.Integer(private),
        })

    else:
        raise ValueError(pretty_message(
            '''
            key_type must be one of "public", "private", not %s
            ''',
            repr(key_type)
        ))