def filter_by_milestone(self, filtered_issues, tag_name, all_issues):
        """
        :param list(dict) filtered_issues: Filtered issues.
        :param str tag_name: Name (title) of tag.
        :param list(dict) all_issues: All issues.
        :rtype: list(dict)
        :return: Filtered issues according milestone.
        """

        filtered_issues = self.remove_issues_in_milestones(filtered_issues)
        if tag_name:
            # add missed issues (according milestones)
            issues_to_add = self.find_issues_to_add(all_issues, tag_name)
            filtered_issues.extend(issues_to_add)
        return filtered_issues