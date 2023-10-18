def send(self, url, http_method, **client_args):
        """
        Make the actual request to the API
        :param url: URL
        :param http_method: The method used to make the request to the API
        :param client_args: Arguments to be sent to the auth client
        :return: requests' response object
        """
        return self.client.send(url, http_method, **client_args)