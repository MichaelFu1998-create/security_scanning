def list(self, **kwargs):
        """Return a list of roles.

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
        data, self.endpoint = self.data_endpoint(kwargs)
        r = super(Resource, self).list(**data)

        # Change display settings and data format for human consumption
        self.configure_display(r)
        return r