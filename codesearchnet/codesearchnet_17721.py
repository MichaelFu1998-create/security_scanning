def build_request(self, path, query_parameters):
        """
        Build the HTTP request by adding query parameters to the path.
        :param path: API endpoint/path to be used.
        :param query_parameters: Query parameters to be added to the request.
        :return: string
        """
        url = 'https://api.uber.com/v1' + self.sanitise_path(path)
        url += '?' + urlencode(query_parameters)

        return url