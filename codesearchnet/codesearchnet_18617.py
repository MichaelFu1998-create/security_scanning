def get_object(self, url):
        """
        Fields to match is a mapping of url params to fields, so for
        the photos example above, it would be:
        
        fields_to_match = { 'object_id': 'id' }
        
        This procedure parses out named params from a URL and then uses
        the fields_to_match dictionary to generate a query.
        """
        params = self.get_params(url)
        query = {}
        for key, value in self._meta.fields_to_match.iteritems():
            try:
                query[value] = params[key]
            except KeyError:
                raise OEmbedException('%s was not found in the urlpattern parameters.  Valid names are: %s' % (key, ', '.join(params.keys())))
        
        try:
            obj = self.get_queryset().get(**query)
        except self._meta.model.DoesNotExist:
            raise OEmbedException('Requested object not found')
        
        return obj