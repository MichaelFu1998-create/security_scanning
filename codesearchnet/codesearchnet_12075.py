def close_cursor(self, handle):
        '''
        Closes the cursor specified and removes it from the `self.cursors`
        dictionary.

        '''

        if handle in self.cursors:
            self.cursors[handle].close()
        else:
            raise KeyError('cursor with handle %s was not found' % handle)