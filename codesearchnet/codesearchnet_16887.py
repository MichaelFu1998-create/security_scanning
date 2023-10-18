def append(self, key, value=MARKER, replace=True):
        '''
        Append the item to the metadata.
        '''
        return self.add_item(key, value, replace=replace)