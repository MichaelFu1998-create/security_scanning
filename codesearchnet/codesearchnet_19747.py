def unseal(self, data, return_options=False):
        '''Unseal data'''

        data = self._remove_magic(data)
        data = urlsafe_nopadding_b64decode(data)
        options = self._read_header(data)
        data = self._add_magic(data)
        data = self._unsign_data(data, options)
        data = self._remove_magic(data)
        data = self._remove_header(data, options)
        data = self._decrypt_data(data, options)
        data = self._decompress_data(data, options)
        data = self._unserialize_data(data, options)

        if return_options:
            return data, options
        else:
            return data