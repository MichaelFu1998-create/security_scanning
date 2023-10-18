def _decode(self, data, algorithm, key=None):
        '''Decode data with specific algorithm'''

        if algorithm['type'] == 'hmac':
            verify_signature = data[-algorithm['hash_size']:]
            data = data[:-algorithm['hash_size']]
            signature = self._hmac_generate(data, algorithm, key)
            if not const_equal(verify_signature, signature):
                raise Exception('Invalid signature')
            return data
        elif algorithm['type'] == 'aes':
            return self._aes_decrypt(data, algorithm, key)
        elif algorithm['type'] == 'no-serialization':
            return data
        elif algorithm['type'] == 'json':
            return json.loads(data)
        elif algorithm['type'] == 'no-compression':
            return data
        elif algorithm['type'] == 'gzip':
            return self._zlib_decompress(data, algorithm)
        else:
            raise Exception('Algorithm not supported: %s' % algorithm['type'])