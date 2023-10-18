def delete(self, url=None, post_data={}, parse_data=False, key=None, parameters=None):
        """ Issue a PUT request.

        Kwargs:
            url (str): Destination URL
            post_data (dict): Dictionary of parameter and values
            parse_data (bool): If true, parse response data
            key (string): If parse_data==True, look for this key when parsing data
            parameters (dict): Additional GET parameters to append to the URL

        Returns:
            dict. Response (a dict with keys: success, data, info, body)
        
        Raises:
            AuthenticationError, ConnectionError, urllib2.HTTPError, ValueError, Exception
        """
        return self._fetch("DELETE", url, post_data=post_data, parse_data=parse_data, key=key, parameters=parameters, full_return=True)