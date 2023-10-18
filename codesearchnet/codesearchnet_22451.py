def check_ip(self, ip):
        """
        Check IP trough the httpBL API

        :param ip: ipv4 ip address
        :return: httpBL results or None if any error is occurred
        """

        self._last_result = None

        if is_valid_ipv4(ip):
            key = None
            if self._use_cache:
                key = self._make_cache_key(ip)
                self._last_result = self._cache.get(key, version=self._cache_version)

            if self._last_result is None:
                # request httpBL API
                error, age, threat, type = self._request_httpbl(ip)
                if error == 127 or error == 0:
                    self._last_result = {
                        'error': error,
                        'age': age,
                        'threat': threat,
                        'type': type
                    }
                    if self._use_cache:
                        self._cache.set(key, self._last_result, timeout=self._api_timeout, version=self._cache_version)
            if self._last_result is not None and settings.CACHED_HTTPBL_USE_LOGGING:
                logger.info(
                    'httpBL check ip: {0}; '
                    'httpBL result: error: {1}, age: {2}, threat: {3}, type: {4}'.format(ip,
                                                                                         self._last_result['error'],
                                                                                         self._last_result['age'],
                                                                                         self._last_result['threat'],
                                                                                         self._last_result['type']
                                                                                         )
                )

        return self._last_result