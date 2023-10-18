def get_all(self, **kwargs):
        '''Get all concepts from all providers.

        .. code-block:: python

            # get all concepts in all providers.
            registry.get_all()

            # get all concepts in all providers.
            # If possible, display the results with a Dutch label.
            registry.get_all(language='nl')

        :param string language: Optional. If present, it should be a
            :term:`language-tag`. This language-tag is passed on to the
            underlying providers and used when selecting the label to display
            for each concept.

        :returns: a list of :class:`dict`.
            Each dict has two keys: id and concepts.
        '''
        kwarguments = {}
        if 'language' in kwargs:
            kwarguments['language'] = kwargs['language']
        return [{'id': p.get_vocabulary_id(), 'concepts': p.get_all(**kwarguments)}
                for p in self.providers.values()]