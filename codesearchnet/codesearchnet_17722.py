def get_json(self, uri_path, http_method='GET', query_parameters=None, body=None, headers=None):
        """
        Fetches the JSON returned, after making the call and checking for errors.
        :param uri_path: Endpoint to be used to make a request.
        :param http_method: HTTP method to be used.
        :param query_parameters: Parameters to be added to the request.
        :param body: Optional body, if required.
        :param headers: Optional headers, if required.
        :return: JSON
        """
        query_parameters = query_parameters or {}
        headers = headers or {}

        # Add credentials to the request
        query_parameters = self.add_credentials(query_parameters)

        # Build the request uri with parameters
        uri = self.build_request(uri_path, query_parameters)

        if http_method in ('POST', 'PUT', 'DELETE') and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        headers['Accept'] = 'application/json'
        response, content = self.client.request(
            uri=uri,
            method=http_method,
            body=body,
            headers=headers
        )

        # Check for known errors that could be returned
        self.check_status(content, response)

        return json.loads(content.decode('utf-8'))