def _advapi32_sign(private_key, data, hash_algorithm, rsa_pss_padding=False):
    """
    Generates an RSA, DSA or ECDSA signature via CryptoAPI

    :param private_key:
        The PrivateKey to generate the signature with

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha256", "sha384", "sha512" or "raw"

    :param rsa_pss_padding:
        If PSS padding should be used for RSA keys

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the signature
    """

    algo = private_key.algorithm

    if algo == 'rsa' and hash_algorithm == 'raw':
        padded_data = add_pkcs1v15_signature_padding(private_key.byte_size, data)
        return raw_rsa_private_crypt(private_key, padded_data)

    if algo == 'rsa' and rsa_pss_padding:
        hash_length = {
            'sha1': 20,
            'sha224': 28,
            'sha256': 32,
            'sha384': 48,
            'sha512': 64
        }.get(hash_algorithm, 0)
        padded_data = add_pss_padding(hash_algorithm, hash_length, private_key.bit_size, data)
        return raw_rsa_private_crypt(private_key, padded_data)

    if private_key.algorithm == 'dsa' and hash_algorithm == 'md5':
        raise ValueError(pretty_message(
            '''
            Windows does not support md5 signatures with DSA keys
            '''
        ))

    hash_handle = None

    try:
        alg_id = {
            'md5': Advapi32Const.CALG_MD5,
            'sha1': Advapi32Const.CALG_SHA1,
            'sha256': Advapi32Const.CALG_SHA_256,
            'sha384': Advapi32Const.CALG_SHA_384,
            'sha512': Advapi32Const.CALG_SHA_512,
        }[hash_algorithm]

        hash_handle_pointer = new(advapi32, 'HCRYPTHASH *')
        res = advapi32.CryptCreateHash(
            private_key.context_handle,
            alg_id,
            null(),
            0,
            hash_handle_pointer
        )
        handle_error(res)

        hash_handle = unwrap(hash_handle_pointer)

        res = advapi32.CryptHashData(hash_handle, data, len(data), 0)
        handle_error(res)

        out_len = new(advapi32, 'DWORD *')
        res = advapi32.CryptSignHashW(
            hash_handle,
            Advapi32Const.AT_SIGNATURE,
            null(),
            0,
            null(),
            out_len
        )
        handle_error(res)

        buffer_length = deref(out_len)
        buffer_ = buffer_from_bytes(buffer_length)

        res = advapi32.CryptSignHashW(
            hash_handle,
            Advapi32Const.AT_SIGNATURE,
            null(),
            0,
            buffer_,
            out_len
        )
        handle_error(res)

        output = bytes_from_buffer(buffer_, deref(out_len))

        # CryptoAPI outputs the signature in little endian byte order, so we
        # must swap it for compatibility with other systems
        output = output[::-1]

        if algo == 'dsa':
            # Switch the two integers because the reversal just before switched
            # then
            half_len = len(output) // 2
            output = output[half_len:] + output[:half_len]
            # Windows doesn't use the ASN.1 Sequence for DSA signatures,
            # so we have to convert it here for the verification to work
            output = algos.DSASignature.from_p1363(output).dump()

        return output

    finally:
        if hash_handle:
            advapi32.CryptDestroyHash(hash_handle)