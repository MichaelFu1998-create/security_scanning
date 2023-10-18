def _bcrypt_load_key(key_object, key_info, container, curve_name):
    """
    Loads a certificate, public key or private key into a Certificate,
    PublicKey or PrivateKey object via CNG

    :param key_object:
        An asn1crypto.x509.Certificate, asn1crypto.keys.PublicKeyInfo or
        asn1crypto.keys.PrivateKeyInfo object

    :param key_info:
        An asn1crypto.keys.PublicKeyInfo or asn1crypto.keys.PrivateKeyInfo
        object

    :param container:
        The class of the object to hold the key_handle

    :param curve_name:
        None or a unicode string of the curve name for an EC key

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        oscrypto.errors.AsymmetricKeyError - when the key is incompatible with the OS crypto library
        OSError - when an error is returned by the OS crypto library

    :return:
        A PrivateKey, PublicKey or Certificate object, based on container
    """

    alg_handle = None
    key_handle = None

    key_type = 'public' if isinstance(key_info, keys.PublicKeyInfo) else 'private'
    algo = key_info.algorithm

    try:
        alg_selector = key_info.curve[1] if algo == 'ec' else algo
        alg_constant = {
            'rsa': BcryptConst.BCRYPT_RSA_ALGORITHM,
            'dsa': BcryptConst.BCRYPT_DSA_ALGORITHM,
            'secp256r1': BcryptConst.BCRYPT_ECDSA_P256_ALGORITHM,
            'secp384r1': BcryptConst.BCRYPT_ECDSA_P384_ALGORITHM,
            'secp521r1': BcryptConst.BCRYPT_ECDSA_P521_ALGORITHM,
        }[alg_selector]
        alg_handle = open_alg_handle(alg_constant)

        if algo == 'rsa':
            if key_type == 'public':
                blob_type = BcryptConst.BCRYPT_RSAPUBLIC_BLOB
                magic = BcryptConst.BCRYPT_RSAPUBLIC_MAGIC
                parsed_key = key_info['public_key'].parsed
                prime1_size = 0
                prime2_size = 0
            else:
                blob_type = BcryptConst.BCRYPT_RSAFULLPRIVATE_BLOB
                magic = BcryptConst.BCRYPT_RSAFULLPRIVATE_MAGIC
                parsed_key = key_info['private_key'].parsed
                prime1 = int_to_bytes(parsed_key['prime1'].native)
                prime2 = int_to_bytes(parsed_key['prime2'].native)
                exponent1 = int_to_bytes(parsed_key['exponent1'].native)
                exponent2 = int_to_bytes(parsed_key['exponent2'].native)
                coefficient = int_to_bytes(parsed_key['coefficient'].native)
                private_exponent = int_to_bytes(parsed_key['private_exponent'].native)
                prime1_size = len(prime1)
                prime2_size = len(prime2)

            public_exponent = int_to_bytes(parsed_key['public_exponent'].native)
            modulus = int_to_bytes(parsed_key['modulus'].native)

            blob_struct_pointer = struct(bcrypt, 'BCRYPT_RSAKEY_BLOB')
            blob_struct = unwrap(blob_struct_pointer)
            blob_struct.Magic = magic
            blob_struct.BitLength = key_info.bit_size
            blob_struct.cbPublicExp = len(public_exponent)
            blob_struct.cbModulus = len(modulus)
            blob_struct.cbPrime1 = prime1_size
            blob_struct.cbPrime2 = prime2_size

            blob = struct_bytes(blob_struct_pointer) + public_exponent + modulus
            if key_type == 'private':
                blob += prime1 + prime2
                blob += fill_width(exponent1, prime1_size)
                blob += fill_width(exponent2, prime2_size)
                blob += fill_width(coefficient, prime1_size)
                blob += fill_width(private_exponent, len(modulus))

        elif algo == 'dsa':
            if key_type == 'public':
                blob_type = BcryptConst.BCRYPT_DSA_PUBLIC_BLOB
                public_key = key_info['public_key'].parsed.native
                params = key_info['algorithm']['parameters']
            else:
                blob_type = BcryptConst.BCRYPT_DSA_PRIVATE_BLOB
                public_key = key_info.public_key.native
                private_bytes = int_to_bytes(key_info['private_key'].parsed.native)
                params = key_info['private_key_algorithm']['parameters']

            public_bytes = int_to_bytes(public_key)
            p = int_to_bytes(params['p'].native)
            g = int_to_bytes(params['g'].native)
            q = int_to_bytes(params['q'].native)

            if key_info.bit_size > 1024:
                q_len = len(q)
            else:
                q_len = 20

            key_width = max(len(public_bytes), len(g), len(p))

            public_bytes = fill_width(public_bytes, key_width)
            p = fill_width(p, key_width)
            g = fill_width(g, key_width)
            q = fill_width(q, q_len)
            # We don't know the count or seed, so we set them to the max value
            # since setting them to 0 results in a parameter error
            count = b'\xff' * 4
            seed = b'\xff' * q_len

            if key_info.bit_size > 1024:
                if key_type == 'public':
                    magic = BcryptConst.BCRYPT_DSA_PUBLIC_MAGIC_V2
                else:
                    magic = BcryptConst.BCRYPT_DSA_PRIVATE_MAGIC_V2

                blob_struct_pointer = struct(bcrypt, 'BCRYPT_DSA_KEY_BLOB_V2')
                blob_struct = unwrap(blob_struct_pointer)
                blob_struct.dwMagic = magic
                blob_struct.cbKey = key_width
                # We don't know if SHA256 was used here, but the output is long
                # enough for the generation of q for the supported 2048/224,
                # 2048/256 and 3072/256 FIPS approved pairs
                blob_struct.hashAlgorithm = BcryptConst.DSA_HASH_ALGORITHM_SHA256
                blob_struct.standardVersion = BcryptConst.DSA_FIPS186_3
                blob_struct.cbSeedLength = q_len
                blob_struct.cbGroupSize = q_len
                blob_struct.Count = byte_array(count)

                blob = struct_bytes(blob_struct_pointer)
                blob += seed + q + p + g + public_bytes
                if key_type == 'private':
                    blob += fill_width(private_bytes, q_len)

            else:
                if key_type == 'public':
                    magic = BcryptConst.BCRYPT_DSA_PUBLIC_MAGIC
                else:
                    magic = BcryptConst.BCRYPT_DSA_PRIVATE_MAGIC

                blob_struct_pointer = struct(bcrypt, 'BCRYPT_DSA_KEY_BLOB')
                blob_struct = unwrap(blob_struct_pointer)
                blob_struct.dwMagic = magic
                blob_struct.cbKey = key_width
                blob_struct.Count = byte_array(count)
                blob_struct.Seed = byte_array(seed)
                blob_struct.q = byte_array(q)

                blob = struct_bytes(blob_struct_pointer) + p + g + public_bytes
                if key_type == 'private':
                    blob += fill_width(private_bytes, q_len)

        elif algo == 'ec':
            if key_type == 'public':
                blob_type = BcryptConst.BCRYPT_ECCPUBLIC_BLOB
                public_key = key_info['public_key']
            else:
                blob_type = BcryptConst.BCRYPT_ECCPRIVATE_BLOB
                public_key = key_info.public_key
                private_bytes = int_to_bytes(key_info['private_key'].parsed['private_key'].native)

            blob_struct_pointer = struct(bcrypt, 'BCRYPT_ECCKEY_BLOB')
            blob_struct = unwrap(blob_struct_pointer)

            magic = {
                ('public', 'secp256r1'): BcryptConst.BCRYPT_ECDSA_PUBLIC_P256_MAGIC,
                ('public', 'secp384r1'): BcryptConst.BCRYPT_ECDSA_PUBLIC_P384_MAGIC,
                ('public', 'secp521r1'): BcryptConst.BCRYPT_ECDSA_PUBLIC_P521_MAGIC,
                ('private', 'secp256r1'): BcryptConst.BCRYPT_ECDSA_PRIVATE_P256_MAGIC,
                ('private', 'secp384r1'): BcryptConst.BCRYPT_ECDSA_PRIVATE_P384_MAGIC,
                ('private', 'secp521r1'): BcryptConst.BCRYPT_ECDSA_PRIVATE_P521_MAGIC,
            }[(key_type, curve_name)]

            key_width = {
                'secp256r1': 32,
                'secp384r1': 48,
                'secp521r1': 66
            }[curve_name]

            x, y = public_key.to_coords()

            x_bytes = int_to_bytes(x)
            y_bytes = int_to_bytes(y)

            x_bytes = fill_width(x_bytes, key_width)
            y_bytes = fill_width(y_bytes, key_width)

            blob_struct.dwMagic = magic
            blob_struct.cbKey = key_width

            blob = struct_bytes(blob_struct_pointer) + x_bytes + y_bytes
            if key_type == 'private':
                blob += fill_width(private_bytes, key_width)

        key_handle_pointer = new(bcrypt, 'BCRYPT_KEY_HANDLE *')
        res = bcrypt.BCryptImportKeyPair(
            alg_handle,
            null(),
            blob_type,
            key_handle_pointer,
            blob,
            len(blob),
            BcryptConst.BCRYPT_NO_KEY_VALIDATION
        )
        handle_error(res)

        key_handle = unwrap(key_handle_pointer)
        return container(key_handle, key_object)

    finally:
        if alg_handle:
            close_alg_handle(alg_handle)