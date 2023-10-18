def read(self, pk=None, fail_on_no_results=False, fail_on_multiple_results=False, **kwargs):
        """
        =====API DOCS=====
        Retrieve and return objects from the Ansible Tower API.

        :param pk: Primary key of the resource to be read. Tower CLI will only attempt to read that object
                   if ``pk`` is provided (not ``None``).
        :type pk: int
        :param fail_on_no_results: Flag that if set, zero results is considered a failure case and raises
                                   an exception; otherwise, empty list is returned. (Note: This is always True
                                   if a primary key is included.)
        :type fail_on_no_results: bool
        :param fail_on_multiple_results: Flag that if set, at most one result is expected, and more results
                                         constitutes a failure case. (Note: This is meaningless if a primary
                                         key is included, as there can never be multiple results.)
        :type fail_on_multiple_results: bool
        :param query: Contains 2-tuples used as query parameters to filter resulting resource objects.
        :type query: list
        :param `**kwargs`: Keyword arguments which, all together, will be used as query parameters to filter
                           resulting resource objects.
        :returns: loaded JSON from Tower backend response body.
        :rtype: dict
        :raises tower_cli.exceptions.BadRequest: When 2-tuples in ``query`` overlaps key-value pairs in
                                                 ``**kwargs``.
        :raises tower_cli.exceptions.NotFound: When no objects are found and ``fail_on_no_results`` flag is on.
        :raises tower_cli.exceptions.MultipleResults: When multiple objects are found and
                                                      ``fail_on_multiple_results`` flag is on.

        =====API DOCS=====
        """
        # Piece together the URL we will be hitting.
        url = self.endpoint
        if pk:
            url += '%s/' % pk

        # Pop the query parameter off of the keyword arguments; it will
        # require special handling (below).
        queries = kwargs.pop('query', [])

        # Remove default values (anything where the value is None).
        self._pop_none(kwargs)

        # Remove fields that are specifically excluded from lookup
        for field in self.fields:
            if field.no_lookup and field.name in kwargs:
                kwargs.pop(field.name)

        # If queries were provided, process them.
        params = list(kwargs.items())
        for query in queries:
            params.append((query[0], query[1]))

        # Make the request to the Ansible Tower API.
        r = client.get(url, params=params)
        resp = r.json()

        # If this was a request with a primary key included, then at the
        # point that we got a good result, we know that we're done and can
        # return the result.
        if pk:
            # Make the results all look the same, for easier parsing
            # by other methods.
            #
            # Note that the `get` method will effectively undo this operation,
            # but that's a good thing, because we might use `get` without a
            # primary key.
            return {'count': 1, 'results': [resp]}

        # Did we get zero results back when we shouldn't?
        # If so, this is an error, and we need to complain.
        if fail_on_no_results and resp['count'] == 0:
            raise exc.NotFound('The requested object could not be found.')

        # Did we get more than one result back?
        # If so, this is also an error, and we need to complain.
        if fail_on_multiple_results and resp['count'] >= 2:
            raise exc.MultipleResults('Expected one result, got %d. Possibly caused by not providing required '
                                      'fields. Please tighten your criteria.' % resp['count'])

        # Return the response.
        return resp