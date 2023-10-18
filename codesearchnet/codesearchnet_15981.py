def request(self, path, method=None, data={}):
        """sends a request and gets a response from the Plivo REST API

        path: the URL (relative to the endpoint URL, after the /v1
        method: the HTTP method to use, defaults to POST
        data: for POST or PUT, a dict of data to send

        returns Plivo response in XML or raises an exception on error
        """
        if not path:
            raise ValueError('Invalid path parameter')
        if method and method not in ['GET', 'POST', 'DELETE', 'PUT']:
            raise NotImplementedError(
                'HTTP %s method not implemented' % method)

        if path[0] == '/':
            uri = self.url + path
        else:
            uri = self.url + '/' + path

        if APPENGINE:
            return json.loads(self._appengine_fetch(uri, data, method))
        return json.loads(self._urllib2_fetch(uri, data, method))