def read(self, *args, **kwargs):
        '''
        Do extra processing so we can display the actor field as
        a top-level field
        '''
        if 'actor' in kwargs:
            kwargs['actor'] = kwargs.pop('actor')
        r = super(Resource, self).read(*args, **kwargs)
        if 'results' in r:
            for d in r['results']:
                self._promote_actor(d)
        else:
            self._promote_actor(d)
        return r