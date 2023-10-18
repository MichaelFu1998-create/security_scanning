def traverse_pagination(response, endpoint, content_filter_query, query_params):
        """
        Traverse a paginated API response and extracts and concatenates "results" returned by API.

        Arguments:
            response (dict): API response object.
            endpoint (Slumber.Resource): API endpoint object.
            content_filter_query (dict): query parameters used to filter catalog results.
            query_params (dict): query parameters used to paginate results.

        Returns:
            list: all the results returned by the API.
        """
        results = response.get('results', [])

        page = 1
        while response.get('next'):
            page += 1
            response = endpoint().post(content_filter_query, **dict(query_params, page=page))
            results += response.get('results', [])

        return results