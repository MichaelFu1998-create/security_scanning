def _do_request(self, method, slug, **kwargs):
        """
        Does HTTP request sending / response validation.
        Prevents RequestExceptions from propagating
        """
        # ensure we are configured
        if not self.configured:
            self.configure()

        url = self._make_url(slug)

        # 'defaults' are values associated with every request.
        # following will make values in kwargs override them.
        defaults = {"headers": self.auth_header, "params": self.params}
        for item in defaults.keys():
            # override default's value with kwargs's one if existing.
            kwargs[item] = dict(defaults[item], **(kwargs.get(item, {})))

        # request() can raise connectivity related exceptions.
        # raise_for_status raises an exception ONLY if the response
        # status_code is "not-OK" i.e 4XX, 5XX..
        #
        # All of these inherit from RequestException
        # which is "translated" into an APIError.
        try:
            resp = request(method, url, **kwargs)
            resp.raise_for_status()
        except RequestException as e:
            reason = "HTTP {0} request to {1} failed: {2}"
            raise APIError(reason.format(method, url, repr(e)))
        return resp