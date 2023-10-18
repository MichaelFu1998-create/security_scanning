def execute(self, timeout=None):
        """Execute all currently queued batch commands"""
        logger.debug(' > Batch API request (length %s)' % len(self._commands))

        auth = self._build_http_auth()

        headers = self._build_request_headers()
        logger.debug('\tbatch headers: %s' % headers)

        logger.debug('\tbatch command length: %s' % len(self._commands))

        path = self._build_request_path(self.BATCH_ENDPOINT)

        data = json.dumps(self._commands, cls=self._json_encoder)
        r = requests.post(
            path,
            auth=auth,
            headers=headers,
            data=data,
            timeout=(self.DEFAULT_TIMEOUT if timeout is None else timeout)
        )

        self._commands = []

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return r