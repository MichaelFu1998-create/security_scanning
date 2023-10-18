def list(self, **kwargs):
        """Return a list of objects.

        =====API DOCS=====
        Retrieve a list of Tower settings.

        :param category: The category slug in which to look up indevidual settings.
        :type category: str
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource objects.
        :returns: A JSON object containing details of all resource objects returned by Tower backend.
        :rtype: dict

        =====API DOCS=====
        """
        self.custom_category = kwargs.get('category', 'all')
        try:
            result = super(Resource, self).list(**kwargs)
        except exc.NotFound as e:
            categories = map(
                lambda category: category['slug'],
                client.get('/settings/').json()['results']
            )
            e.message = '%s is not a valid category.  Choose from [%s]' % (
                kwargs['category'],
                ', '.join(categories)
            )
            raise e
        finally:
            self.custom_category = None
        return {
            'results': [{'id': k, 'value': v} for k, v in result.items()]
        }