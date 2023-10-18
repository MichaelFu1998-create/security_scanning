def filter_by_labels(self, all_issues, kind):
        """
        Filter issues for include/exclude labels.

        :param list(dict) all_issues: All issues.
        :param str kind: Either "issues" or "pull requests".
        :rtype: list(dict)
        :return: Filtered issues.
        """

        filtered_issues = self.include_issues_by_labels(all_issues)
        filtered = self.exclude_issues_by_labels(filtered_issues)
        if self.options.verbose > 1:
            print("\tremaining {}: {}".format(kind, len(filtered)))
        return filtered