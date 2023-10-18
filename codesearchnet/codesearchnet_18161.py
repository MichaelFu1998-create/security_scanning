def send(self, relative_path, http_method, **requests_args):
        """
        Subclasses must implement this method, that will be used to send API requests with proper auth
        :param relative_path: URL path relative to self.base_url
        :param http_method: HTTP method
        :param requests_args: kargs to be sent to requests
        :return:
        """
        url = urljoin(self.base_url, relative_path)

        return self.session.request(http_method, url, **requests_args)