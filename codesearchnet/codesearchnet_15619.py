def include_issues_by_labels(self, all_issues):
        """
        Include issues with labels, specified in self.options.include_labels.

        :param list(dict) all_issues: All issues.
        :rtype: list(dict)
        :return: Filtered issues.
        """

        included_by_labels = self.filter_by_include_labels(all_issues)
        wo_labels = self.filter_wo_labels(all_issues)
        il = set([f["number"] for f in included_by_labels])
        wl = set([w["number"] for w in wo_labels])
        filtered_issues = []
        for issue in all_issues:
            if issue["number"] in il or issue["number"] in wl:
                filtered_issues.append(issue)
        return filtered_issues