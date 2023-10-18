def decrypt(encrypted_privkey, passphrase):
    """BIP0038 non-ec-multiply decryption. Returns WIF privkey.

    :param Base58 encrypted_privkey: Private key
    :param str passphrase: UTF-8 encoded passphrase for decryption
    :return: BIP0038 non-ec-multiply decrypted key
    :rtype: Base58
    :raises SaltException: if checksum verification failed (e.g. wrong
        password)

    """

    d = unhexlify(base58decode(encrypted_privkey))
    d = d[2:]  # remove trailing 0x01 and 0x42
    flagbyte = d[0:1]  # get flag byte
    d = d[1:]  # get payload
    assert flagbyte == b"\xc0", "Flagbyte has to be 0xc0"
    salt = d[0:4]
    d = d[4:-4]
    if SCRYPT_MODULE == "scrypt":  # pragma: no cover
        key = scrypt.hash(passphrase, salt, 16384, 8, 8)
    elif SCRYPT_MODULE == "pylibscrypt":  # pragma: no cover
        key = scrypt.scrypt(bytes(passphrase, "utf-8"), salt, 16384, 8, 8)
    else:
        raise ValueError("No scrypt module loaded")  # pragma: no cover
    derivedhalf1 = key[0:32]
    derivedhalf2 = key[32:64]
    encryptedhalf1 = d[0:16]
    encryptedhalf2 = d[16:32]
    aes = AES.new(derivedhalf2, AES.MODE_ECB)
    decryptedhalf2 = aes.decrypt(encryptedhalf2)
    decryptedhalf1 = aes.decrypt(encryptedhalf1)
    privraw = decryptedhalf1 + decryptedhalf2
    privraw = "%064x" % (int(hexlify(privraw), 16) ^ int(hexlify(derivedhalf1), 16))
    wif = Base58(privraw)
    """ Verify Salt """
    privkey = PrivateKey(format(wif, "wif"))
    addr = format(privkey.bitcoin.address, "BTC")
    a = _bytes(addr)
    saltverify = hashlib.sha256(hashlib.sha256(a).digest()).digest()[0:4]
    if saltverify != salt:  # pragma: no cover
        raise SaltException("checksum verification failed! Password may be incorrect.")
    return wif