def search(self, **kwargs):
        '''Query this object (and its descendants).

        Parameters
        ----------
        kwargs
            Each `(key, value)` pair encodes a search field in `key`
            and a target value in `value`.

            `key` must be a string, and should correspond to a property in
            the JAMS object hierarchy, e.g., 'Annotation.namespace` or `email`

            `value` must be either an object (tested for equality), a
            string describing a search pattern (regular expression), or a
            lambda function which evaluates to `True` if the candidate
            object matches the search criteria and `False` otherwise.

        Returns
        -------
        match : bool
            `True` if any of the search keys match the specified value,
            `False` otherwise, or if the search keys do not exist
            within the object.

        Examples
        --------
        >>> J = jams.JObject(foo=5, needle='quick brown fox')
        >>> J.search(needle='.*brown.*')
        True
        >>> J.search(needle='.*orange.*')
        False
        >>> J.search(badger='.*brown.*')
        False
        >>> J.search(foo=5)
        True
        >>> J.search(foo=10)
        False
        >>> J.search(foo=lambda x: x < 10)
        True
        >>> J.search(foo=lambda x: x > 10)
        False
        '''

        match = False

        r_query = {}
        myself = self.__class__.__name__

        # Pop this object name off the query
        for k, value in six.iteritems(kwargs):
            k_pop = query_pop(k, myself)

            if k_pop:
                r_query[k_pop] = value

        if not r_query:
            return False

        for key in r_query:
            if hasattr(self, key):
                match |= match_query(getattr(self, key), r_query[key])

        if not match:
            for attr in dir(self):
                obj = getattr(self, attr)

                if isinstance(obj, JObject):
                    match |= obj.search(**r_query)

        return match