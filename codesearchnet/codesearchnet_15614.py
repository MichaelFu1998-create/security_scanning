def exclude_issues_by_labels(self, issues):
        """
        Delete all issues with labels from exclude-labels option.

        :param list(dict) issues: All issues for tag.
        :rtype: list(dict)
        :return: Filtered issues.
        """
        if not self.options.exclude_labels:
            return copy.deepcopy(issues)

        remove_issues = set()
        exclude_labels = self.options.exclude_labels
        include_issues = []
        for issue in issues:
            for label in issue["labels"]:
                if label["name"] in exclude_labels:
                    remove_issues.add(issue["number"])
                    break
        for issue in issues:
            if issue["number"] not in remove_issues:
                include_issues.append(issue)
        return include_issues