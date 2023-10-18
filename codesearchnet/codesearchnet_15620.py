def filter_wo_labels(self, all_issues):
        """
        Filter all issues that don't have a label.

        :rtype: list(dict)
        :return: Issues without labels.
        """

        issues_wo_labels = []
        if not self.options.add_issues_wo_labels:
            for issue in all_issues:
                if not issue['labels']:
                    issues_wo_labels.append(issue)
        return issues_wo_labels