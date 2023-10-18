def send(self, relative_path, http_method, **requests_args):
        """
        Make a unauthorized request
        :param relative_path: URL path relative to self.base_url
        :param http_method: HTTP method
        :param requests_args: kargs to be sent to requests
        :return: requests' response object
        """
        if http_method != "get":
            warnings.warn(_("You are using methods other than get with no authentication!!!"))

        return super(NoAuthClient, self).send(relative_path, http_method, **requests_args)