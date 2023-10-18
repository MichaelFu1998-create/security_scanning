def get_queries(parameters):
        """
        Get a list of all queries (q=... parameters) from an URL parameter string
        :param parameters: The url parameter list
        """
        parsed_params = urlparse.parse_qs(parameters)
        if 'q' not in parsed_params:
            return []
        queries = parsed_params['q']

        # Check if only one query string is given
        # in this case make it a list
        if not isinstance(queries, list):
            queries = [queries]
        return queries