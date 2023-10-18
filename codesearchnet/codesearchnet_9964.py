def _setup_evp_encrypt_decrypt(cipher, data):
    """
    Creates an EVP_CIPHER pointer object and determines the buffer size
    necessary for the parameter specified.

    :param evp_cipher_ctx:
        An EVP_CIPHER_CTX pointer

    :param cipher:
        A unicode string of "aes128", "aes192", "aes256", "des",
        "tripledes_2key", "tripledes_3key", "rc2", "rc4"

    :param key:
        The key byte string

    :param data:
        The plaintext or ciphertext as a byte string

    :param padding:
        If padding is to be used

    :return:
        A 2-element tuple with the first element being an EVP_CIPHER pointer
        and the second being an integer that is the required buffer size
    """

    evp_cipher = {
        'aes128': libcrypto.EVP_aes_128_cbc,
        'aes192': libcrypto.EVP_aes_192_cbc,
        'aes256': libcrypto.EVP_aes_256_cbc,
        'rc2': libcrypto.EVP_rc2_cbc,
        'rc4': libcrypto.EVP_rc4,
        'des': libcrypto.EVP_des_cbc,
        'tripledes_2key': libcrypto.EVP_des_ede_cbc,
        'tripledes_3key': libcrypto.EVP_des_ede3_cbc,
    }[cipher]()

    if cipher == 'rc4':
        buffer_size = len(data)
    else:
        block_size = {
            'aes128': 16,
            'aes192': 16,
            'aes256': 16,
            'rc2': 8,
            'des': 8,
            'tripledes_2key': 8,
            'tripledes_3key': 8,
        }[cipher]
        buffer_size = block_size * int(math.ceil(len(data) / block_size))

    return (evp_cipher, buffer_size)