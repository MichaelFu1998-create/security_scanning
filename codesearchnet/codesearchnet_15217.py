def generate(self, **kwargs):
        '''
        Generate a :term:`URI` based on parameters passed.

        :param id: The id of the concept or collection.
        :param type: What we're generating a :term:`URI` for: `concept`
            or `collection`.
        :rtype: string
        '''
        if kwargs['type'] not in ['concept', 'collection']:
            raise ValueError('Type %s is invalid' % kwargs['type'])
        return (
            self.pattern % (self.vocabulary_id, kwargs['type'], kwargs['id'])
        ).lower()