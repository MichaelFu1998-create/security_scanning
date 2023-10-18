def remove_issues_in_milestones(self, filtered_issues):
        """
        :param list(dict) filtered_issues: Filtered issues.
        :rtype: list(dict)
        :return: List with removed issues, that contain milestones with
                 same name as a tag.
        """
        for issue in filtered_issues:
            # leave issues without milestones
            if issue["milestone"]:
                # check, that this milestone is in tag list:
                for tag in self.filtered_tags:
                    if tag["name"] == issue["milestone"]["title"]:
                        filtered_issues.remove(issue)
        return filtered_issues