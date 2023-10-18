def get_by_uri(self, uri):
        '''Get a concept or collection by its uri.

        Returns a single concept or collection if one exists with this uri.
        Returns False otherwise.

        :param string uri: The uri to find a concept or collection for.
        :raises ValueError: The uri is invalid.
        :rtype: :class:`skosprovider.skos.Concept` or
            :class:`skosprovider.skos.Collection`
        '''
        if not is_uri(uri):
            raise ValueError('%s is not a valid URI.' % uri)
        # Check if there's a provider that's more likely to have the URI
        csuris = [csuri for csuri in self.concept_scheme_uri_map.keys() if uri.startswith(csuri)]
        for csuri in csuris:
            c = self.get_provider(csuri).get_by_uri(uri)
            if c:
                return c
        # Check all providers
        for p in self.providers.values():
            c = p.get_by_uri(uri)
            if c:
                return c
        return False