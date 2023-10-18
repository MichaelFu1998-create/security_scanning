def request(self, method, parameters=None, file_payload=None):
        """
        Do the generic processing of a request to the server.

        If file_payload is specified, it will be PUT to the server.

        :param method: Desired API method
        :type method: string
        :param parameters: (optional) Parameters to pass in the HTTP body
        :type parameters: None | dict[string, string]
        :param file_payload: (optional) File-like object to be sent with the
            HTTP request
        :type file_payload: None | file | FileIO
        :returns: Dictionary representing the JSON response to the request
        :rtype: dict
        :raises pydas.exceptions.PydasException: if the request failed
        """
        method_url = self.full_url + method
        response = None

        try:
            if file_payload:
                response = requests.put(method_url,
                                        data=file_payload.read(),
                                        params=parameters,
                                        allow_redirects=True,
                                        verify=self._verify_ssl_certificate,
                                        auth=self.auth)
            else:
                response = requests.post(method_url,
                                         params=parameters,
                                         allow_redirects=True,
                                         verify=self._verify_ssl_certificate,
                                         auth=self.auth)

        except requests.exceptions.SSLError:
            exception = pydas.exceptions.SSLVerificationFailed(
                'Request failed with an SSL verification error')
            exception.method = method
            exception.request = response.request
            raise exception

        except requests.exceptions.ConnectionError:
            exception = pydas.exceptions.RequestError(
                'Request failed with a connection error')
            exception.method = method
            if response is not None:
                exception.request = response.request
            raise exception

        status_code = response.status_code

        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            error_code = None
            message = 'Request failed with HTTP status code {0}'.format(
                status_code)

            try:
                content = response.json()

                if 'code' in content:
                    error_code = int(content['code'])
                    message = 'Request failed with HTTP status code {0}, ' \
                        'Midas Server error code {1}, and response content ' \
                        '{2}'.format(status_code, error_code, response.content)

            except ValueError:
                pass

            exception = pydas.exceptions \
                .get_exception_from_status_and_error_codes(status_code,
                                                           error_code,
                                                           message)
            exception.code = error_code
            exception.method = method
            exception.response = response
            raise exception

        try:
            content = response.json()

        except ValueError:
            exception = pydas.exceptions.ParseError(
                'Request failed with HTTP status code {0} and response '
                'content {1}'.format(status_code, response.content))
            exception.method = method
            exception.response = response
            raise exception

        if 'stat' not in content:
            exception = pydas.exceptions.ParseError(
                'Request failed with HTTP status code {0} and response '
                'content {1}'.format(status_code, response.content))
            exception.method = method
            raise exception

        if content['stat'] != 'ok':
            if 'code' in content:
                error_code = int(content['code'])
                message = 'Request failed with HTTP status code {0}, Midas ' \
                    'Server error code {1}, and response content {2}' \
                    .format(status_code, error_code, response.content)
            else:
                error_code = None
                message = 'Request failed with HTTP status code {0} and ' \
                    'response content {1}'.format(status_code,
                                                  response.content)

            exception = pydas.exceptions \
                .get_exception_from_status_and_error_codes(status_code,
                                                           error_code,
                                                           message)
            exception.method = method
            exception.response = response
            raise exception

        if 'data' not in content:
            exception = pydas.exceptions.ParseError(
                'Request failed with HTTP status code {0} and response '
                'content {1}'.format(status_code, response.content))
            exception.method = method
            exception.response = response
            raise exception

        return content['data']