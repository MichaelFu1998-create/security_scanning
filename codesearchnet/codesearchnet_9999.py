def _advapi32_verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding=False):
    """
    Verifies an RSA, DSA or ECDSA signature via CryptoAPI

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to verify the signature with

    :param signature:
        A byte string of the signature to verify

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha256", "sha384", "sha512" or "raw"

    :param rsa_pss_padding:
        If PSS padding should be used for RSA keys

    :raises:
        oscrypto.errors.SignatureError - when the signature is determined to be invalid
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library
    """

    algo = certificate_or_public_key.algorithm

    if algo == 'rsa' and rsa_pss_padding:
        hash_length = {
            'sha1': 20,
            'sha224': 28,
            'sha256': 32,
            'sha384': 48,
            'sha512': 64
        }.get(hash_algorithm, 0)
        decrypted_signature = raw_rsa_public_crypt(certificate_or_public_key, signature)
        key_size = certificate_or_public_key.bit_size
        if not verify_pss_padding(hash_algorithm, hash_length, key_size, data, decrypted_signature):
            raise SignatureError('Signature is invalid')
        return

    if algo == 'rsa' and hash_algorithm == 'raw':
        padded_plaintext = raw_rsa_public_crypt(certificate_or_public_key, signature)
        try:
            plaintext = remove_pkcs1v15_signature_padding(certificate_or_public_key.byte_size, padded_plaintext)
            if not constant_compare(plaintext, data):
                raise ValueError()
        except (ValueError):
            raise SignatureError('Signature is invalid')
        return

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
            certificate_or_public_key.context_handle,
            alg_id,
            null(),
            0,
            hash_handle_pointer
        )
        handle_error(res)

        hash_handle = unwrap(hash_handle_pointer)

        res = advapi32.CryptHashData(hash_handle, data, len(data), 0)
        handle_error(res)

        if algo == 'dsa':
            # Windows doesn't use the ASN.1 Sequence for DSA signatures,
            # so we have to convert it here for the verification to work
            try:
                signature = algos.DSASignature.load(signature).to_p1363()
                # Switch the two integers so that the reversal later will
                # result in the correct order
                half_len = len(signature) // 2
                signature = signature[half_len:] + signature[:half_len]
            except (ValueError, OverflowError, TypeError):
                raise SignatureError('Signature is invalid')

        # The CryptoAPI expects signatures to be in little endian byte order,
        # which is the opposite of other systems, so we must reverse it
        reversed_signature = signature[::-1]

        res = advapi32.CryptVerifySignatureW(
            hash_handle,
            reversed_signature,
            len(signature),
            certificate_or_public_key.key_handle,
            null(),
            0
        )
        handle_error(res)

    finally:
        if hash_handle:
            advapi32.CryptDestroyHash(hash_handle)