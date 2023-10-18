def filter_by_include_labels(self, issues):
        """
        Filter issues to include only issues with labels
        specified in include_labels.

        :param list(dict) issues: Pre-filtered issues.
        :rtype: list(dict)
        :return: Filtered issues.
        """

        if not self.options.include_labels:
            return copy.deepcopy(issues)
        filtered_issues = []
        include_labels = set(self.options.include_labels)
        for issue in issues:
            labels = [label["name"] for label in issue["labels"]]
            if include_labels.intersection(labels):
                filtered_issues.append(issue)
        return filtered_issues