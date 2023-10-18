def delete(self, endpoint, data, url_data=None, parameters=None):
        """Returns the response and body for a delete request
            endpoints = 'users'  # resource to access
            data = {'username': 'blah, 'password': blah}  # DELETE body
            url_data = {}, ()  # Used to modularize endpoints, see __init__
            parameters = {}, ((),()) # URL paramters, ex: google.com?q=a&f=b
        """
        return self.request_handler.request(
            self._url(endpoint, url_data, parameters),
            method=Api._method['delete'],
            body=urllib.urlencode(data)
        )