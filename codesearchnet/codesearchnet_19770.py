def _aes_decrypt(data, algorithm, key):
        '''AES decrypt'''

        if algorithm['subtype'] == 'cbc':
            mode = AES.MODE_CBC
        else:
            raise Exception('AES subtype not supported: %s'
                            % algorithm['subtype'])

        iv_size = algorithm['iv_size']

        if 'iv' in algorithm and algorithm['iv']:
            if len(algorithm['iv']) != algorithm['iv_size']:
                raise Exception('Invalid IV size')
            iv_value = algorithm['iv']
            enc = data
        else:
            iv_value = data[:iv_size]
            enc = data[iv_size:]

        dec = AES.new(key, mode, iv_value).decrypt(enc)

        numpad = ord(dec[-1])
        dec = dec[0:-numpad]

        return dec