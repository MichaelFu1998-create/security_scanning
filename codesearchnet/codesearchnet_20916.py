def get(self, url=None, parse_data=True, key=None, parameters=None):
        """ Issue a GET request.

        Kwargs:
            url (str): Destination URL
            parse_data (bool): If true, parse response data
            key (string): If parse_data==True, look for this key when parsing data
            parameters (dict): Additional GET parameters to append to the URL

        Returns:
            dict. Response (a dict with keys: success, data, info, body)

        Raises:
            AuthenticationError, ConnectionError, urllib2.HTTPError, ValueError, Exception
        """
        return self._fetch("GET", url, post_data=None, parse_data=parse_data, key=key, parameters=parameters)