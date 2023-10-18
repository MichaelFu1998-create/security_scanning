def query(self, search_function, attribute=None):
        """Query the list

        Parameters
        ----------
        search_function : a string, regular expression or function
            Used to find the matching elements in the list.
            - a regular expression (possibly compiled), in which case the
            given attribute of the object should match the regular expression.
            - a function which takes one argument and returns True for
            desired values

        attribute : string or None
            the name attribute of the object to passed as argument to the
            `search_function`. If this is None, the object itself is used.

        Returns
        -------
        DictList
            a new list of objects which match the query

        Examples
        --------
        >>> import cobra.test
        >>> model = cobra.test.create_test_model('textbook')
        >>> model.reactions.query(lambda x: x.boundary)
        >>> import re
        >>> regex = re.compile('^g', flags=re.IGNORECASE)
        >>> model.metabolites.query(regex, attribute='name')
        """
        def select_attribute(x):
            if attribute is None:
                return x
            else:
                return getattr(x, attribute)

        try:
            # if the search_function is a regular expression
            regex_searcher = re.compile(search_function)

            if attribute is not None:
                matches = (
                    i for i in self if
                    regex_searcher.findall(select_attribute(i)) != [])

            else:
                # Don't regex on objects
                matches = (
                    i for i in self if
                    regex_searcher.findall(getattr(i, 'id')) != [])

        except TypeError:
            matches = (
                i for i in self if search_function(select_attribute(i)))

        results = self.__class__()
        results._extend_nocheck(matches)
        return results