def _unarmor_pem_openssl_private(headers, data, password):
    """
    Parses a PKCS#1 private key, or encrypted private key

    :param headers:
        A dict of "Name: Value" lines from right after the PEM header

    :param data:
        A byte string of the DER-encoded PKCS#1 private key

    :param password:
        A byte string of the password to use if the private key is encrypted

    :return:
        A byte string of the DER-encoded private key
    """

    enc_algo = None
    enc_iv_hex = None
    enc_iv = None

    if 'DEK-Info' in headers:
        params = headers['DEK-Info']
        if params.find(',') != -1:
            enc_algo, enc_iv_hex = params.strip().split(',')
        else:
            enc_algo = 'RC4'

    if not enc_algo:
        return data

    if enc_iv_hex:
        enc_iv = binascii.unhexlify(enc_iv_hex.encode('ascii'))
    enc_algo = enc_algo.lower()

    enc_key_length = {
        'aes-128-cbc': 16,
        'aes-128': 16,
        'aes-192-cbc': 24,
        'aes-192': 24,
        'aes-256-cbc': 32,
        'aes-256': 32,
        'rc4': 16,
        'rc4-64': 8,
        'rc4-40': 5,
        'rc2-64-cbc': 8,
        'rc2-40-cbc': 5,
        'rc2-cbc': 16,
        'rc2': 16,
        'des-ede3-cbc': 24,
        'des-ede3': 24,
        'des3': 24,
        'des-ede-cbc': 16,
        'des-cbc': 8,
        'des': 8,
    }[enc_algo]

    enc_key = hashlib.md5(password + enc_iv[0:8]).digest()
    while enc_key_length > len(enc_key):
        enc_key += hashlib.md5(enc_key + password + enc_iv[0:8]).digest()
    enc_key = enc_key[0:enc_key_length]

    enc_algo_name = {
        'aes-128-cbc': 'aes',
        'aes-128': 'aes',
        'aes-192-cbc': 'aes',
        'aes-192': 'aes',
        'aes-256-cbc': 'aes',
        'aes-256': 'aes',
        'rc4': 'rc4',
        'rc4-64': 'rc4',
        'rc4-40': 'rc4',
        'rc2-64-cbc': 'rc2',
        'rc2-40-cbc': 'rc2',
        'rc2-cbc': 'rc2',
        'rc2': 'rc2',
        'des-ede3-cbc': 'tripledes',
        'des-ede3': 'tripledes',
        'des3': 'tripledes',
        'des-ede-cbc': 'tripledes',
        'des-cbc': 'des',
        'des': 'des',
    }[enc_algo]
    decrypt_func = crypto_funcs[enc_algo_name]

    if enc_algo_name == 'rc4':
        return decrypt_func(enc_key, data)

    return decrypt_func(enc_key, data, enc_iv)