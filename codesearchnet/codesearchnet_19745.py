def set_magic(self, magic):
        '''Set magic (prefix)'''
        if magic is None or isinstance(magic, str):
            self.magic = magic
        else:
            raise TypeError('Invalid value for magic')