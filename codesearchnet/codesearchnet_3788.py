def list(self, all_pages=False, **kwargs):
        """Return a list of notification templates.

        Note here configuration-related fields like
        'notification_configuration' and 'channels' will not be
        used even provided.

        If one or more filters are provided through keyword arguments,
        filter the results accordingly.

        If no filters are provided, return all results.

        =====API DOCS=====
        Retrieve a list of objects.

        :param all_pages: Flag that if set, collect all pages of content from the API when returning results.
        :type all_pages: bool
        :param page: The page to show. Ignored if all_pages is set.
        :type page: int
        :param query: Contains 2-tuples used as query parameters to filter resulting resource objects.
        :type query: list
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource objects.
        :returns: A JSON object containing details of all resource objects returned by Tower backend.
        :rtype: dict

        =====API DOCS=====
        """
        self._separate(kwargs)
        return super(Resource, self).list(all_pages=all_pages, **kwargs)