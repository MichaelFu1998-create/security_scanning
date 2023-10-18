def _bcrypt_interpret_ec_key_blob(key_type, blob_struct, blob):
    """
    Take a CNG BCRYPT_ECCKEY_BLOB and converts it into an ASN.1 structure

    :param key_type:
        A unicode string of "private" or "public"

    :param blob_struct:
        An instance of BCRYPT_ECCKEY_BLOB

    :param blob:
        A byte string of the binary data contained after the struct

    :return:
        An asn1crypto.keys.PrivateKeyInfo or asn1crypto.keys.PublicKeyInfo
        object, based on the key_type param
    """

    magic = native(int, blob_struct.dwMagic)
    key_byte_length = native(int, blob_struct.cbKey)

    curve = {
        BcryptConst.BCRYPT_ECDSA_PRIVATE_P256_MAGIC: 'secp256r1',
        BcryptConst.BCRYPT_ECDSA_PRIVATE_P384_MAGIC: 'secp384r1',
        BcryptConst.BCRYPT_ECDSA_PRIVATE_P521_MAGIC: 'secp521r1',
        BcryptConst.BCRYPT_ECDSA_PUBLIC_P256_MAGIC: 'secp256r1',
        BcryptConst.BCRYPT_ECDSA_PUBLIC_P384_MAGIC: 'secp384r1',
        BcryptConst.BCRYPT_ECDSA_PUBLIC_P521_MAGIC: 'secp521r1',
    }[magic]

    public = b'\x04' + blob[0:key_byte_length * 2]

    if key_type == 'public':
        return keys.PublicKeyInfo({
            'algorithm': keys.PublicKeyAlgorithm({
                'algorithm': 'ec',
                'parameters': keys.ECDomainParameters(
                    name='named',
                    value=curve
                )
            }),
            'public_key': public,
        })

    elif key_type == 'private':
        private = int_from_bytes(blob[key_byte_length * 2:key_byte_length * 3])
        return keys.PrivateKeyInfo({
            'version': 0,
            'private_key_algorithm': keys.PrivateKeyAlgorithm({
                'algorithm': 'ec',
                'parameters': keys.ECDomainParameters(
                    name='named',
                    value=curve
                )
            }),
            'private_key': keys.ECPrivateKey({
                'version': 'ecPrivkeyVer1',
                'private_key': private,
                'public_key': public,
            }),
        })

    else:
        raise ValueError(pretty_message(
            '''
            key_type must be one of "public", "private", not %s
            ''',
            repr(key_type)
        ))