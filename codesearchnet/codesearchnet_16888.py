def extend(self, items, replace=True):
        '''
        Append the items to the metadata.
        '''
        if isinstance(items, dict) or isinstance(items, SortableDict):
            items = list(items.items())

        for (key, value) in items:
            self.append(key, value, replace=replace)