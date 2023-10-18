def remove_provider(self, id):
        '''
        Remove the provider with the given id or :term:`URI`.

        :param str id: The identifier for the provider.
        :returns: A :class:`skosprovider.providers.VocabularyProvider` or
            `False` if the id is unknown.
        '''
        if id in self.providers:
            p = self.providers.get(id, False)
            del self.providers[id]
            del self.concept_scheme_uri_map[p.concept_scheme.uri]
            return p
        elif id in self.concept_scheme_uri_map:
            id = self.concept_scheme_uri_map[id]
            return self.remove_provider(id)
        else:
            return False