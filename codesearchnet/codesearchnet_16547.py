def create_url(self, path, params={}, opts={}):
        """
        Create URL with supplied path and `opts` parameters dict.

        Parameters
        ----------
        path : str
        opts : dict
            Dictionary specifying URL parameters. Non-imgix parameters are
            added to the URL unprocessed. For a complete list of imgix
            supported parameters, visit https://docs.imgix.com/apis/url .
            (default {})

        Returns
        -------
        str
            imgix URL
        """

        if opts:
            warnings.warn('`opts` has been deprecated. Use `params` instead.',
                          DeprecationWarning, stacklevel=2)
        params = params or opts
        if self._shard_strategy == SHARD_STRATEGY_CRC:
            crc = zlib.crc32(path.encode('utf-8')) & 0xffffffff
            index = crc % len(self._domains)  # Deterministically choose domain
            domain = self._domains[index]

        elif self._shard_strategy == SHARD_STRATEGY_CYCLE:
            domain = self._domains[self._shard_next_index]
            self._shard_next_index = (
                self._shard_next_index + 1) % len(self._domains)

        else:
            domain = self._domains[0]

        scheme = "https" if self._use_https else "http"

        url_obj = UrlHelper(
            domain,
            path,
            scheme,
            sign_key=self._sign_key,
            include_library_param=self._include_library_param,
            params=params)

        return str(url_obj)