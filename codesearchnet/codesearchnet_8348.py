def encrypt(privkey, passphrase):
    """ BIP0038 non-ec-multiply encryption. Returns BIP0038 encrypted privkey.

    :param privkey: Private key
    :type privkey: Base58
    :param str passphrase: UTF-8 encoded passphrase for encryption
    :return: BIP0038 non-ec-multiply encrypted wif key
    :rtype: Base58

    """
    if isinstance(privkey, str):
        privkey = PrivateKey(privkey)
    else:
        privkey = PrivateKey(repr(privkey))

    privkeyhex = repr(privkey)  # hex
    addr = format(privkey.bitcoin.address, "BTC")
    a = _bytes(addr)
    salt = hashlib.sha256(hashlib.sha256(a).digest()).digest()[0:4]
    if SCRYPT_MODULE == "scrypt":  # pragma: no cover
        key = scrypt.hash(passphrase, salt, 16384, 8, 8)
    elif SCRYPT_MODULE == "pylibscrypt":  # pragma: no cover
        key = scrypt.scrypt(bytes(passphrase, "utf-8"), salt, 16384, 8, 8)
    else:  # pragma: no cover
        raise ValueError("No scrypt module loaded")  # pragma: no cover
    (derived_half1, derived_half2) = (key[:32], key[32:])
    aes = AES.new(derived_half2, AES.MODE_ECB)
    encrypted_half1 = _encrypt_xor(privkeyhex[:32], derived_half1[:16], aes)
    encrypted_half2 = _encrypt_xor(privkeyhex[32:], derived_half1[16:], aes)
    " flag byte is forced 0xc0 because Graphene only uses compressed keys "
    payload = b"\x01" + b"\x42" + b"\xc0" + salt + encrypted_half1 + encrypted_half2
    " Checksum "
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    privatkey = hexlify(payload + checksum).decode("ascii")
    return Base58(privatkey)