def get_catalog_results(self, content_filter_query, query_params=None, traverse_pagination=False):
        """
        Return results from the discovery service's search/all endpoint.

        Arguments:
            content_filter_query (dict): query parameters used to filter catalog results.
            query_params (dict): query parameters used to paginate results.
            traverse_pagination (bool): True to return all results, False to return the paginated response.
                                        Defaults to False.

        Returns:
            dict: Paginated response or all the records.
        """
        query_params = query_params or {}

        try:
            endpoint = getattr(self.client, self.SEARCH_ALL_ENDPOINT)
            response = endpoint().post(data=content_filter_query, **query_params)
            if traverse_pagination:
                response['results'] = self.traverse_pagination(response, endpoint, content_filter_query, query_params)
                response['next'] = response['previous'] = None
        except Exception as ex:  # pylint: disable=broad-except
            LOGGER.exception(
                'Attempted to call course-discovery search/all/ endpoint with the following parameters: '
                'content_filter_query: %s, query_params: %s, traverse_pagination: %s. '
                'Failed to retrieve data from the catalog API. content -- [%s]',
                content_filter_query,
                query_params,
                traverse_pagination,
                getattr(ex, 'content', '')
            )
            # We need to bubble up failures when we encounter them instead of masking them!
            raise ex

        return response