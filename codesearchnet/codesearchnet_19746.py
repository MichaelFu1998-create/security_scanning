def seal(self, data, options=None):
        '''Seal data'''

        options = self._set_options(options)

        data = self._serialize_data(data, options)
        data = self._compress_data(data, options)
        data = self._encrypt_data(data, options)
        data = self._add_header(data, options)
        data = self._add_magic(data)
        data = self._sign_data(data, options)
        data = self._remove_magic(data)
        data = urlsafe_nopadding_b64encode(data)
        data = self._add_magic(data)

        return data