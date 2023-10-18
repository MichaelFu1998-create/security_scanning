def step1_get_device_and_user_codes(self, http=None):
        """Returns a user code and the verification URL where to enter it

        Returns:
            A user code as a string for the user to authorize the application
            An URL as a string where the user has to enter the code
        """
        if self.device_uri is None:
            raise ValueError('The value of device_uri must not be None.')

        body = urllib.parse.urlencode({
            'client_id': self.client_id,
            'scope': self.scope,
        })
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        if self.user_agent is not None:
            headers['user-agent'] = self.user_agent

        if http is None:
            http = transport.get_http_object()

        resp, content = transport.request(
            http, self.device_uri, method='POST', body=body, headers=headers)
        content = _helpers._from_bytes(content)
        if resp.status == http_client.OK:
            try:
                flow_info = json.loads(content)
            except ValueError as exc:
                raise OAuth2DeviceCodeError(
                    'Could not parse server response as JSON: "{0}", '
                    'error: "{1}"'.format(content, exc))
            return DeviceFlowInfo.FromResponse(flow_info)
        else:
            error_msg = 'Invalid response {0}.'.format(resp.status)
            try:
                error_dict = json.loads(content)
                if 'error' in error_dict:
                    error_msg += ' Error: {0}'.format(error_dict['error'])
            except ValueError:
                # Couldn't decode a JSON response, stick with the
                # default message.
                pass
            raise OAuth2DeviceCodeError(error_msg)