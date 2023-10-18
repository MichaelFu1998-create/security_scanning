def get_grouped_issues(self, keyfunc=None, sortby=None):
        """
        Retrieves the issues in the collection grouped into buckets according
        to the key generated by the keyfunc.

        :param keyfunc:
            a function that will be used to generate the key that identifies
            the group that an issue will be assigned to. This function receives
            a single tidypy.Issue argument and must return a string. If not
            specified, the filename of the issue will be used.
        :type keyfunc: func
        :param sortby: the properties to sort the issues by
        :type sortby: list(str)
        :rtype: OrderedDict
        """

        if not keyfunc:
            keyfunc = default_group
        if not sortby:
            sortby = self.DEFAULT_SORT
        self._ensure_cleaned_issues()
        return self._group_issues(self._cleaned_issues, keyfunc, sortby)