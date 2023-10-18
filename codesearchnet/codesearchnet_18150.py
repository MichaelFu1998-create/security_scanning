def _req(self, url, method='GET', **kw):
        '''Make request and convert JSON response to python objects'''
        send = requests.post if method == 'POST' else requests.get
        try:
            r = send(
                url,
                headers=self._token_header(),
                timeout=self.settings['timeout'],
                **kw)
        except requests.exceptions.Timeout:
            raise ApiError('Request timed out (%s seconds)' % self.settings['timeout'])
        try:
            json = r.json()
        except ValueError:
            raise ApiError('Received not JSON response from API')
        if json.get('status') != 'ok':
            raise ApiError('API error: received unexpected json from API: %s' % json)
        return json