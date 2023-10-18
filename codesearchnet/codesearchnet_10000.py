def _bcrypt_verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding=False):
    """
    Verifies an RSA, DSA or ECDSA signature via CNG

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

    if hash_algorithm == 'raw':
        digest = data
    else:
        hash_constant = {
            'md5': BcryptConst.BCRYPT_MD5_ALGORITHM,
            'sha1': BcryptConst.BCRYPT_SHA1_ALGORITHM,
            'sha256': BcryptConst.BCRYPT_SHA256_ALGORITHM,
            'sha384': BcryptConst.BCRYPT_SHA384_ALGORITHM,
            'sha512': BcryptConst.BCRYPT_SHA512_ALGORITHM
        }[hash_algorithm]
        digest = getattr(hashlib, hash_algorithm)(data).digest()

    padding_info = null()
    flags = 0

    if certificate_or_public_key.algorithm == 'rsa':
        if rsa_pss_padding:
            flags = BcryptConst.BCRYPT_PAD_PSS
            padding_info_struct_pointer = struct(bcrypt, 'BCRYPT_PSS_PADDING_INFO')
            padding_info_struct = unwrap(padding_info_struct_pointer)
            # This has to be assigned to a variable to prevent cffi from gc'ing it
            hash_buffer = buffer_from_unicode(hash_constant)
            padding_info_struct.pszAlgId = cast(bcrypt, 'wchar_t *', hash_buffer)
            padding_info_struct.cbSalt = len(digest)
        else:
            flags = BcryptConst.BCRYPT_PAD_PKCS1
            padding_info_struct_pointer = struct(bcrypt, 'BCRYPT_PKCS1_PADDING_INFO')
            padding_info_struct = unwrap(padding_info_struct_pointer)
            # This has to be assigned to a variable to prevent cffi from gc'ing it
            if hash_algorithm == 'raw':
                padding_info_struct.pszAlgId = null()
            else:
                hash_buffer = buffer_from_unicode(hash_constant)
                padding_info_struct.pszAlgId = cast(bcrypt, 'wchar_t *', hash_buffer)
        padding_info = cast(bcrypt, 'void *', padding_info_struct_pointer)
    else:
        # Windows doesn't use the ASN.1 Sequence for DSA/ECDSA signatures,
        # so we have to convert it here for the verification to work
        try:
            signature = algos.DSASignature.load(signature).to_p1363()
        except (ValueError, OverflowError, TypeError):
            raise SignatureError('Signature is invalid')

    res = bcrypt.BCryptVerifySignature(
        certificate_or_public_key.key_handle,
        padding_info,
        digest,
        len(digest),
        signature,
        len(signature),
        flags
    )
    failure = res == BcryptConst.STATUS_INVALID_SIGNATURE
    failure = failure or res == BcryptConst.STATUS_INVALID_PARAMETER
    if failure:
        raise SignatureError('Signature is invalid')

    handle_error(res)