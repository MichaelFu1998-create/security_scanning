def filter_issues_for_tags(self, newer_tag, older_tag):
        """
        Apply all filters to issues and pull requests.

        :param dict older_tag: All issues before this tag's date will be
                               excluded. May be special value, if new tag is
                               the first tag. (Means **older_tag** is when
                               the repo  was created.)
        :param dict newer_tag: All issues after this tag's date  will be
                               excluded. May be title of unreleased section.
        :rtype: list(dict), list(dict)
        :return: Filtered issues and pull requests.
        """

        filtered_pull_requests = self.delete_by_time(self.pull_requests,
                                                     older_tag, newer_tag)
        filtered_issues = self.delete_by_time(self.issues, older_tag,
                                              newer_tag)

        newer_tag_name = newer_tag["name"] if newer_tag else None

        if self.options.filter_issues_by_milestone:
            # delete excess irrelevant issues (according milestones).Issue #22.
            filtered_issues = self.filter_by_milestone(
                filtered_issues, newer_tag_name, self.issues
            )
            filtered_pull_requests = self.filter_by_milestone(
                filtered_pull_requests, newer_tag_name, self.pull_requests
            )
        return filtered_issues, filtered_pull_requests