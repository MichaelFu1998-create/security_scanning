def list(self, all_pages=False, **kwargs):
        """Return a list of objects.

        If one or more filters are provided through keyword arguments, filter the results accordingly.

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
        # TODO: Move to a field callback method to make it generic
        # If multiple statuses where given, add OR queries for each of them
        if kwargs.get('status', None) and ',' in kwargs['status']:
            all_status = kwargs.pop('status').strip(',').split(',')
            queries = list(kwargs.pop('query', ()))
            for status in all_status:
                if status in STATUS_CHOICES:
                    queries.append(('or__status', status))
                else:
                    raise exc.TowerCLIError('This status does not exist: {}'.format(status))
            kwargs['query'] = tuple(queries)

        # If the `all_pages` flag is set, then ignore any page that might also be sent.
        if all_pages:
            kwargs.pop('page', None)
            kwargs.pop('page_size', None)

        # Get the response.
        debug.log('Getting records.', header='details')
        response = self.read(**kwargs)

        # Convert next and previous to int
        self._convert_pagenum(response)

        # If we were asked for all pages, keep retrieving pages until we have them all.
        if all_pages and response['next']:
            cursor = copy(response)
            while cursor['next']:
                cursor = self.read(**dict(kwargs, page=cursor['next']))
                self._convert_pagenum(cursor)
                response['results'] += cursor['results']
                response['count'] += cursor['count']
            response['next'] = None

        # Done; return the response
        return response