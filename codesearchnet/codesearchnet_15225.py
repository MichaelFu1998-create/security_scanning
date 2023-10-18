def find(self, query, **kwargs):
        '''Launch a query across all or a selection of providers.

        .. code-block:: python

            # Find anything that has a label of church in any provider.
            registry.find({'label': 'church'})

            # Find anything that has a label of church with the BUILDINGS provider.
            # Attention, this syntax was deprecated in version 0.3.0
            registry.find({'label': 'church'}, providers=['BUILDINGS'])

            # Find anything that has a label of church with the BUILDINGS provider.
            registry.find({'label': 'church'}, providers={'ids': ['BUILDINGS']})

            # Find anything that has a label of church with a provider
            # marked with the subject 'architecture'.
            registry.find({'label': 'church'}, providers={'subject': 'architecture'})

            # Find anything that has a label of church in any provider.
            # If possible, display the results with a Dutch label.
            registry.find({'label': 'church'}, language='nl')

        :param dict query: The query parameters that will be passed on to each
            :meth:`~skosprovider.providers.VocabularyProvider.find` method of
            the selected.
            :class:`providers <skosprovider.providers.VocabularyProvider>`.
        :param dict providers: Optional. If present, it should be a dictionary.
            This dictionary can contain any of the keyword arguments available
            to the :meth:`get_providers` method. The query will then only
            be passed to the providers confirming to these arguments.
        :param string language: Optional. If present, it should be a
            :term:`language-tag`. This language-tag is passed on to the
            underlying providers and used when selecting the label to display
            for each concept.
        :returns: a list of :class:`dict`.
            Each dict has two keys: id and concepts.
        '''
        if 'providers' not in kwargs:
            providers = self.get_providers()
        else:
            pargs = kwargs['providers']
            if isinstance(pargs, list):
                providers = self.get_providers(ids=pargs)
            else:
                providers = self.get_providers(**pargs)
        kwarguments = {}
        if 'language' in kwargs:
            kwarguments['language'] = kwargs['language']
        return [{'id': p.get_vocabulary_id(), 'concepts': p.find(query, **kwarguments)}
                for p in providers]