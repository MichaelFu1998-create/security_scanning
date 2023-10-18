def delete_by_time(self, issues, older_tag, newer_tag):
        """
        Filter issues that belong to specified tag range.

        :param list(dict) issues: Issues to filter.
        :param dict older_tag: All issues before this tag's date will be
                               excluded. May be special value, if **newer_tag**
                               is the first tag. (Means **older_tag** is when
                               the repo was created.)
        :param dict newer_tag: All issues after this tag's date  will be
                               excluded. May be title of unreleased section.
        :rtype: list(dict)
        :return: Filtered issues.
        """

        if not older_tag and not newer_tag:
            # in case if no tags are specified - return unchanged array
            return copy.deepcopy(issues)

        newer_tag_time = self.get_time_of_tag(newer_tag)
        older_tag_time = self.get_time_of_tag(older_tag)
        filtered = []
        for issue in issues:
            if issue.get('actual_date'):
                rslt = older_tag_time < issue['actual_date'] <= newer_tag_time
                if rslt:
                    filtered.append(copy.deepcopy(issue))
        return filtered