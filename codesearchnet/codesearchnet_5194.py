def __perform_request(self, url, type=GET, params=None):
        """
            This method will perform the real request,
            in this way we can customize only the "output" of the API call by
            using self.__call_api method.
            This method will return the request object.
        """
        if params is None:
            params = {}

        if not self.token:
            raise TokenError("No token provided. Please use a valid token")

        url = urlparse.urljoin(self.end_point, url)

        # lookup table to find out the appropriate requests method,
        # headers and payload type (json or query parameters)
        identity = lambda x: x
        json_dumps = lambda x: json.dumps(x)
        lookup = {
            GET: (self._session.get, {}, 'params', identity),
            POST: (self._session.post, {'Content-type': 'application/json'}, 'data',
                   json_dumps),
            PUT: (self._session.put, {'Content-type': 'application/json'}, 'data',
                  json_dumps),
            DELETE: (self._session.delete,
                     {'content-type': 'application/json'},
                     'data', json_dumps),
        }

        requests_method, headers, payload, transform = lookup[type]
        agent = "{0}/{1} {2}/{3}".format('python-digitalocean',
                                         __version__,
                                         requests.__name__,
                                         requests.__version__)
        headers.update({'Authorization': 'Bearer ' + self.token,
                        'User-Agent': agent})
        kwargs = {'headers': headers, payload: transform(params)}

        timeout = self.get_timeout()
        if timeout:
            kwargs['timeout'] = timeout

        # remove token from log
        headers_str = str(headers).replace(self.token.strip(), 'TOKEN')
        self._log.debug('%s %s %s:%s %s %s' %
                        (type, url, payload, params, headers_str, timeout))

        return requests_method(url, **kwargs)