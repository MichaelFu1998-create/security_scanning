def list(self, group=None, host_filter=None, **kwargs):
        """Return a list of hosts.

        =====API DOCS=====
        Retrieve a list of hosts.

        :param group: Primary key or name of the group whose hosts will be listed.
        :type group: str
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
        if group:
            kwargs['query'] = kwargs.get('query', ()) + (('groups__in', group),)
        if host_filter:
            kwargs['query'] = kwargs.get('query', ()) + (('host_filter', host_filter),)
        return super(Resource, self).list(**kwargs)