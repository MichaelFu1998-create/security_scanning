def get_providers(self, **kwargs):
        '''Get all providers registered.

        If keyword `ids` is present, get only the providers with these ids.

        If keys `subject` is present, get only the providers that have this subject.

        .. code-block:: python

           # Get all providers with subject 'biology'
           registry.get_providers(subject='biology')

           # Get all providers with id 1 or 2
           registry.get_providers(ids=[1,2])

           # Get all providers with id 1 or 2 and subject 'biology'
           registry.get_providers(ids=[1,2], subject='biology']

        :param list ids: Only return providers with one of the Ids or :term:`URIs <uri>`.
        :param str subject: Only return providers with this subject.
        :returns: A list of :class:`providers <skosprovider.providers.VocabularyProvider>`
        '''
        if 'ids' in kwargs:
            ids = [self.concept_scheme_uri_map.get(id, id) for id in kwargs['ids']]
            providers = [
                self.providers[k] for k in self.providers.keys() if k in ids
            ]
        else:
            providers = list(self.providers.values())
        if 'subject' in kwargs:
            providers = [p for p in providers if kwargs['subject'] in p.metadata['subject']]
        return providers