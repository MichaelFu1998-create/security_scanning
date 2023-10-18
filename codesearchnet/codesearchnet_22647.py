def remove(self, collection, **kwargs):
        '''
        remove records from collection whose parameters match kwargs
        '''
        callback = kwargs.pop('callback')
        yield Op(self.db[collection].remove, kwargs)
        callback()