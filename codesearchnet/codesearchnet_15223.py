def get_provider(self, id):
        '''
        Get a provider by id or :term:`uri`.

        :param str id: The identifier for the provider. This can either be the
            id with which it was registered or the :term:`uri` of the conceptscheme
            that the provider services.
        :returns: A :class:`skosprovider.providers.VocabularyProvider`
            or `False` if the id or uri is unknown.
        '''
        if id in self.providers:
            return self.providers.get(id, False)
        elif is_uri(id) and id in self.concept_scheme_uri_map:
            return self.providers.get(self.concept_scheme_uri_map[id], False)
        return False