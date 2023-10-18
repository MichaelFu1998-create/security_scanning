def get_issues(self, sortby=None):
        """
        Retrieves the issues in the collection.

        :param sortby: the properties to sort the issues by
        :type sortby: list(str)
        :rtype: list(tidypy.Issue)
        """

        self._ensure_cleaned_issues()
        return self._sort_issues(self._cleaned_issues, sortby)