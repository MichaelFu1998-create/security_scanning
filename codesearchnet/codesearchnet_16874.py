def _api_request(self, endpoint, http_method, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Queing batch api request for endpoint: %s' % endpoint)

        path = self._build_request_path(endpoint, absolute=False)
        logger.debug('\tpath: %s' % path)

        data = None
        if 'payload' in kwargs:
            data = kwargs['payload']
        logger.debug('\tdata: %s' % data)

        command = {
            "path": path,
            "method": http_method
        }
        if data:
            command['body'] = data

        self._commands.append(command)