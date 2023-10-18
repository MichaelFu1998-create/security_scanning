def _compose_url(self, url, kwargs):
        """
        Compose a URL starting with the given URL (or self.url if that URL is
        None) and using the values in kwargs.

        :param str url:
            The base URL to use. If None, ``self.url`` will be used instead.
        :param dict kwargs:
            A dictionary of values to override in the base URL. Relevant keys
            will be popped from the dictionary.
        """
        if url is None:
            url = self.url

        if url is None:
            raise ValueError(
                'url not provided and this client has no url attribute')

        split_result = urisplit(url)
        userinfo = split_result.userinfo

        # Build up the kwargs to pass to uricompose
        compose_kwargs = {}
        for key in ['scheme', 'host', 'port', 'path', 'fragment']:
            if key in kwargs:
                compose_kwargs[key] = kwargs.pop(key)
            else:
                compose_kwargs[key] = getattr(split_result, key)

        if 'params' in kwargs:
            compose_kwargs['query'] = kwargs.pop('params')
        else:
            compose_kwargs['query'] = split_result.query

        # Take the userinfo out of the URL and pass as 'auth' to treq so it can
        # be used for HTTP basic auth headers
        if 'auth' not in kwargs and userinfo is not None:
            # treq expects a 2-tuple (username, password)
            kwargs['auth'] = tuple(userinfo.split(':', 2))

        return uricompose(**compose_kwargs)