def generate_dh_parameters(bit_size):
    """
    Generates DH parameters for use with Diffie-Hellman key exchange. Returns
    a structure in the format of DHParameter defined in PKCS#3, which is also
    used by the OpenSSL dhparam tool.

    THIS CAN BE VERY TIME CONSUMING!

    :param bit_size:
        The integer bit size of the parameters to generate. Must be between 512
        and 4096, and divisible by 64. Recommended secure value as of early 2016
        is 2048, with an absolute minimum of 1024.

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        An asn1crypto.algos.DHParameters object. Use
        oscrypto.asymmetric.dump_dh_parameters() to save to disk for usage with
        web servers.
    """

    if not isinstance(bit_size, int_types):
        raise TypeError(pretty_message(
            '''
            bit_size must be an integer, not %s
            ''',
            type_name(bit_size)
        ))

    if bit_size < 512:
        raise ValueError('bit_size must be greater than or equal to 512')

    if bit_size > 4096:
        raise ValueError('bit_size must be less than or equal to 4096')

    if bit_size % 64 != 0:
        raise ValueError('bit_size must be a multiple of 64')

    dh = None

    try:
        dh = libcrypto.DH_new()
        if is_null(dh):
            handle_openssl_error(0)

        result = libcrypto.DH_generate_parameters_ex(dh, bit_size, LibcryptoConst.DH_GENERATOR_2, null())
        handle_openssl_error(result)

        buffer_length = libcrypto.i2d_DHparams(dh, null())
        if buffer_length < 0:
            handle_openssl_error(buffer_length)
        buffer = buffer_from_bytes(buffer_length)
        result = libcrypto.i2d_DHparams(dh, buffer_pointer(buffer))
        if result < 0:
            handle_openssl_error(result)
        dh_params_bytes = bytes_from_buffer(buffer, buffer_length)

        return algos.DHParameters.load(dh_params_bytes)

    finally:
        if dh:
            libcrypto.DH_free(dh)