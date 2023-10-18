def store(self, collection, **kwargs):
        '''
        validate the passed values in kwargs based on the collection,
        store them in the mongodb collection
        '''
        callback = kwargs.pop('callback')
        key = validate(collection, **kwargs)
        data = yield Task(self.fetch, collection, **{key: kwargs[key]})
        if data is not None:
            raise Proauth2Error('duplicate_key')
        yield Op(self.db[collection].insert, kwargs)
        callback()