def verify_signature(self, data):
        '''Verify sealed data signature'''

        data = self._remove_magic(data)
        data = urlsafe_nopadding_b64decode(data)
        options = self._read_header(data)
        data = self._add_magic(data)
        self._unsign_data(data, options)