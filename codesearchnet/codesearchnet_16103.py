def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """
    Implements PBKDF2 with the same API as Django's existing
    implementation, using cryptography.

    :type password: any
    :type salt: any
    :type iterations: int
    :type dklen: int
    :type digest: cryptography.hazmat.primitives.hashes.HashAlgorithm
    """
    if digest is None:
        digest = settings.CRYPTOGRAPHY_DIGEST
    if not dklen:
        dklen = digest.digest_size
    password = force_bytes(password)
    salt = force_bytes(salt)
    kdf = PBKDF2HMAC(
        algorithm=digest,
        length=dklen,
        salt=salt,
        iterations=iterations,
        backend=settings.CRYPTOGRAPHY_BACKEND)
    return kdf.derive(password)