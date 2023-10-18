def set_size(self, size):
        '''
        Size is only set the first time it is called

        Size that is set is returned
        '''
        if self.size is None:
            self.size = size
            return size
        else:
            return self.size