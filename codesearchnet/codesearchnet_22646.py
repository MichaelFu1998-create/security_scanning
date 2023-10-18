def fetch(self, collection, **kwargs):
        '''
        return one record from the collection whose parameters match kwargs
        ---
        kwargs should be a dictionary whose keys match column names (in
        traditional SQL / fields in NoSQL) and whose values are the values of
        those fields.
        e.g. kwargs={name='my application name',client_id=12345}
        '''
        callback = kwargs.pop('callback')
        data = yield Op(self.db[collection].find_one, kwargs)
        callback(data)