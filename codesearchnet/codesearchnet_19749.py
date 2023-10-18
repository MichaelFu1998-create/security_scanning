def _encode(self, data, algorithm, key=None):
        '''Encode data with specific algorithm'''

        if algorithm['type'] == 'hmac':
            return data + self._hmac_generate(data, algorithm, key)
        elif algorithm['type'] == 'aes':
            return self._aes_encrypt(data, algorithm, key)
        elif algorithm['type'] == 'no-serialization':
            return data
        elif algorithm['type'] == 'json':
            return json.dumps(data)
        elif algorithm['type'] == 'no-compression':
            return data
        elif algorithm['type'] == 'gzip':
            return self._zlib_compress(data, algorithm)
        else:
            raise Exception('Algorithm not supported: %s' % algorithm['type'])