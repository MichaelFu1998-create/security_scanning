def _api_call(self, method_name, *args, **kwargs):
        """
        Makes the HTTP request.

        """
        params = kwargs.setdefault('params', {})
        params.update({'key': self._apikey})
        if self._token is not None:
            params.update({'token': self._token})

        http_method = getattr(requests, method_name)
        return http_method(TRELLO_URL + self._url, *args, **kwargs)