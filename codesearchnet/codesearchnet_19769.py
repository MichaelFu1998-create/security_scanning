def _aes_encrypt(data, algorithm, key):
        '''AES encrypt'''

        if algorithm['subtype'] == 'cbc':
            mode = AES.MODE_CBC
        else:
            raise Exception('AES subtype not supported: %s'
                            % algorithm['subtype'])

        iv_size = algorithm['iv_size']
        block_size = iv_size
        include_iv = True

        if 'iv'in algorithm and algorithm['iv']:
            if len(algorithm['iv']) != algorithm['iv_size']:
                raise Exception('Invalid IV size')
            iv_value = algorithm['iv']
            include_iv = False
        else:
            iv_value = get_random_bytes(iv_size)

        numpad = block_size - (len(data) % block_size)
        data = data + numpad * chr(numpad)

        enc = AES.new(key, mode, iv_value).encrypt(data)

        if include_iv:
            enc = iv_value + enc

        return enc