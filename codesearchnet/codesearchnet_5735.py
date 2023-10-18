def FromResponse(cls, response):
        """Create a DeviceFlowInfo from a server response.

        The response should be a dict containing entries as described here:

        http://tools.ietf.org/html/draft-ietf-oauth-v2-05#section-3.7.1
        """
        # device_code, user_code, and verification_url are required.
        kwargs = {
            'device_code': response['device_code'],
            'user_code': response['user_code'],
        }
        # The response may list the verification address as either
        # verification_url or verification_uri, so we check for both.
        verification_url = response.get(
            'verification_url', response.get('verification_uri'))
        if verification_url is None:
            raise OAuth2DeviceCodeError(
                'No verification_url provided in server response')
        kwargs['verification_url'] = verification_url
        # expires_in and interval are optional.
        kwargs.update({
            'interval': response.get('interval'),
            'user_code_expiry': None,
        })
        if 'expires_in' in response:
            kwargs['user_code_expiry'] = (
                _UTCNOW() +
                datetime.timedelta(seconds=int(response['expires_in'])))
        return cls(**kwargs)