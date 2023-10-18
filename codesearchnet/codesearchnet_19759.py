def _remove_magic(self, data):
        '''Verify and remove magic'''

        if not self.magic:
            return data

        magic_size = len(self.magic)
        magic = data[:magic_size]
        if magic != self.magic:
            raise Exception('Invalid magic')
        data = data[magic_size:]

        return data