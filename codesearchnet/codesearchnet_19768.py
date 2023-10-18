def _hmac_generate(data, algorithm, key):
        '''Generate HMAC hash'''

        digestmod = EncryptedPickle._get_hashlib(algorithm['subtype'])

        return HMAC.new(key, data, digestmod).digest()