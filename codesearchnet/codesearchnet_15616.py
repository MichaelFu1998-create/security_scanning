def find_issues_to_add(all_issues, tag_name):
        """
        Add all issues, that should be in that tag, according to milestone.

        :param list(dict) all_issues: All issues.
        :param str tag_name: Name (title) of tag.
        :rtype: List[dict]
        :return: Issues filtered by milestone.
        """

        filtered = []
        for issue in all_issues:
            if issue.get("milestone"):
                if issue["milestone"]["title"] == tag_name:
                    iss = copy.deepcopy(issue)
                    filtered.append(iss)
        return filtered