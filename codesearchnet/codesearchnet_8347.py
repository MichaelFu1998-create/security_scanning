def _encrypt_xor(a, b, aes):
    """ Returns encrypt(a ^ b). """
    a = unhexlify("%0.32x" % (int((a), 16) ^ int(hexlify(b), 16)))
    return aes.encrypt(a)