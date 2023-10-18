def register_provider(self, provider):
        '''
        Register a :class:`skosprovider.providers.VocabularyProvider`.

        :param skosprovider.providers.VocabularyProvider provider: The provider
            to register.
        :raises RegistryException: A provider with this id or uri has already 
            been registered.
        '''
        if provider.get_vocabulary_id() in self.providers:
            raise RegistryException(
                'A provider with this id has already been registered.'
            )
        self.providers[provider.get_vocabulary_id()] = provider
        if provider.concept_scheme.uri in self.concept_scheme_uri_map:
            raise RegistryException(
                'A provider with URI %s has already been registered.' % provider.concept_scheme.uri
            )
        self.concept_scheme_uri_map[provider.concept_scheme.uri] = provider.get_vocabulary_id()