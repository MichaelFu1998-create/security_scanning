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

    alg_handle = None

    # The following algorithm has elements taken from OpenSSL. In short, it
    # generates random numbers and then ensures that they are valid for the
    # hardcoded generator of 2, and then ensures the number is a "safe" prime
    # by ensuring p//2 is prime also.

    # OpenSSL allows use of generator 2 or 5, but we hardcode 2 since it is
    # the default, and what is used by Security.framework on OS X also.
    g = 2

    try:
        byte_size = bit_size // 8
        if _backend == 'win':
            alg_handle = open_alg_handle(BcryptConst.BCRYPT_RNG_ALGORITHM)
            buffer = buffer_from_bytes(byte_size)

        while True:
            if _backend == 'winlegacy':
                rb = os.urandom(byte_size)
            else:
                res = bcrypt.BCryptGenRandom(alg_handle, buffer, byte_size, 0)
                handle_error(res)
                rb = bytes_from_buffer(buffer)

            p = int_from_bytes(rb)

            # If a number is even, it can't be prime
            if p % 2 == 0:
                continue

            # Perform the generator checks outlined in OpenSSL's
            # dh_builtin_genparams() located in dh_gen.c
            if g == 2:
                if p % 24 != 11:
                    continue
            elif g == 5:
                rem = p % 10
                if rem != 3 and rem != 7:
                    continue

            divisible = False
            for prime in _SMALL_PRIMES:
                if p % prime == 0:
                    divisible = True
                    break

            # If the number is not divisible by any of the small primes, then
            # move on to the full Miller-Rabin test.
            if not divisible and _is_prime(bit_size, p):
                q = p // 2
                if _is_prime(bit_size, q):
                    return algos.DHParameters({'p': p, 'g': g})

    finally:
        if alg_handle:
            close_alg_handle(alg_handle)