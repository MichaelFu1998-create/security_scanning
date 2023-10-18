def head(self, endpoint, url_data=None, parameters=None):
        """Returns the response and body for a head request
            endpoints = 'users'  # resource to access
            url_data = {}, ()  # Used to modularize endpoints, see __init__
            parameters = {}, ((),()) # URL paramters, ex: google.com?q=a&f=b
        """
        return self.request_handler.request(
            self._url(endpoint, url_data, parameters),
            method=Api._method['head']
        )