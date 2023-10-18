def _generate_token(self, length=32):
        '''
        _generate_token - internal function for generating randomized alphanumberic
        strings of a given length
        '''
        return ''.join(choice(ascii_letters + digits) for x in range(length))