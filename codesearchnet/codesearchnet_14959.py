def make_request(self, url, method='get', headers=None, data=None,
                     callback=None, errors=STRICT, verify=False, timeout=None, **params):
        """
        Reusable method for performing requests.
        :param url - URL to request
        :param method - request method, default is 'get'
        :param headers - request headers
        :param data - post data
        :param callback - callback to be applied to response,
                          default callback will parse response as json object.
        :param errors - specifies communication errors handling mode, possible
                        values are:
                         * strict (default) - throw an error as soon as one
                            occurred
                         * graceful - ignore certain errors, e.g. EmptyResponse
                         * ignore - ignore all errors and return a result in
                                    any case.
                                    NOTE that it DOES NOT mean that no
                                    exceptions can be
                                    raised from this method, it mostly ignores
                                    communication
                                    related errors.
                         * None or empty string equals to default
        :param verify - whether or not to verify SSL cert, default to False
        :param timeout - the timeout of the request in second, default to None
        :param params - additional query parameters for request
        """
        error_modes = (STRICT, GRACEFUL, IGNORE)
        error_mode = errors or GRACEFUL
        if error_mode.lower() not in error_modes:
            raise ValueError(
                'Possible values for errors argument are: %s'
                % ','.join(error_modes))

        if callback is None:
            callback = self._default_resp_callback

        request = getattr(requests, method.lower())
        log.debug('* Request URL: %s' % url)
        log.debug('* Request method: %s' % method)
        log.debug('* Request query params: %s' % params)
        log.debug('* Request headers: %s' % headers)
        log.debug('* Request timeout: %s' % timeout)

        r = request(
            url, headers=headers, data=data, verify=verify, timeout=timeout, params=params)

        log.debug('* r.url: %s' % r.url)

        try:
            r.raise_for_status()
            return callback(r)
        except Exception as e:
            return self._with_error_handling(r, e,
                                             error_mode, self.response_format)