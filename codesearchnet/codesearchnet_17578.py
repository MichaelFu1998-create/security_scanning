def _url(self, endpoint, url_data=None, parameters=None):
        """Generate URL on the modularized endpoints and url parameters"""
        try:
            url = '%s/%s' % (self.base_url, self.endpoints[endpoint])
        except KeyError:
            raise EndPointDoesNotExist(endpoint)
        if url_data:
            url = url % url_data
        if parameters:
            # url = url?key=value&key=value&key=value...
            url = '%s?%s' % (url, urllib.urlencode(parameters, True))
        return url