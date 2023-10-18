def _get_hashlib(digestmode):
        '''Generate HMAC hash'''
        if digestmode == 'sha1':
            return SHA
        if digestmode == 'sha256':
            return SHA256
        elif digestmode  == 'sha384':
            return SHA384
        elif digestmode == 'sha512':
            return SHA512
        else:
            raise Exception('digestmode not supported: %s'
                            % digestmode)