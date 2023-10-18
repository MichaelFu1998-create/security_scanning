def _api_request(self, endpoint, http_method, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Sending API request to endpoint: %s' % endpoint)

        auth = self._build_http_auth()

        headers = self._build_request_headers(kwargs.get('headers'))
        logger.debug('\theaders: %s' % headers)

        path = self._build_request_path(endpoint)
        logger.debug('\tpath: %s' % path)

        data = self._build_payload(kwargs.get('payload'))
        if not data:
            data = kwargs.get('data')
        logger.debug('\tdata: %s' % data)

        req_kw = dict(
            auth=auth,
            headers=headers,
            timeout=kwargs.get('timeout', self.DEFAULT_TIMEOUT)
        )

        # do some error handling
        if (http_method == self.HTTP_POST):
            if (data):
                r = requests.post(path, data=data, **req_kw)
            else:
                r = requests.post(path, **req_kw)
        elif http_method == self.HTTP_PUT:
            if (data):
                r = requests.put(path, data=data, **req_kw)
            else:
                r = requests.put(path, **req_kw)
        elif http_method == self.HTTP_DELETE:
            r = requests.delete(path, **req_kw)
        else:
            r = requests.get(path, **req_kw)

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return self._parse_response(r)