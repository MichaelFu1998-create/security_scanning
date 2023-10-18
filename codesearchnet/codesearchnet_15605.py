def generate_log_between_tags(self, older_tag, newer_tag):
        """
        Generate log between 2 specified tags.

        :param dict older_tag: All issues before this tag's date will be
                               excluded. May be special value, if new tag is
                               the first tag. (Means **older_tag** is when
                               the repo was created.)
        :param dict newer_tag: All issues after this tag's date  will be
                               excluded. May be title of unreleased section.
        :rtype: str
        :return: Generated ready-to-add tag section for newer tag.
        """

        filtered_issues, filtered_pull_requests = \
            self.filter_issues_for_tags(newer_tag, older_tag)

        older_tag_name = older_tag["name"] if older_tag \
            else self.detect_since_tag()

        if not filtered_issues and not filtered_pull_requests:
            # do not generate an unreleased section if it would be empty
            return ""
        return self.generate_log_for_tag(
            filtered_pull_requests, filtered_issues,
            newer_tag, older_tag_name)