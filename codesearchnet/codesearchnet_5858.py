def _iterate(self, url, **queryparams):
        """
        Iterate over all pages for the given url. Feed in the result of self._build_path as the url.

        :param url: The url of the endpoint
        :type url: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        queryparams['count'] = integer
        queryparams['offset'] = integer
        """
        # fields as a query string parameter should be a string with
        # comma-separated substring values to pass along to
        # self._mc_client._get(). It should also contain total_items whenever
        # the parameter is employed, which is forced here.
        if 'fields' in queryparams:
            if 'total_items' not in queryparams['fields'].split(','):
                queryparams['fields'] += ',total_items'
        # Remove offset and count if provided in queryparams
        # to avoid 'multiple values for keyword argument' TypeError
        queryparams.pop("offset", None)
        queryparams.pop("count", None)
        # Fetch results from mailchimp, up to first 1000
        result = self._mc_client._get(url=url, offset=0, count=1000, **queryparams)
        total = result['total_items']
        # Fetch further results if necessary
        if total > 1000:
            for offset in range(1, int(total / 1000) + 1):
                result = merge_results(result, self._mc_client._get(
                    url=url,
                    offset=int(offset * 1000),
                    count=1000,
                    **queryparams
                ))
            return result
        else:  # Further results not necessary
            return result