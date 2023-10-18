def issue_count(self, include_unclean=False):
        """
        Returns the number of issues in the collection.

        :param include_unclean:
            whether or not to include issues that are being ignored due to
            being a duplicate, excluded, etc.
        :type include_unclean: bool
        :rtype: int
        """

        if include_unclean:
            return len(self._all_issues)
        self._ensure_cleaned_issues()
        return len(self._cleaned_issues)