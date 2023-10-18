def issue_line_with_user(self, line, issue):
        """
        If option author is enabled, a link to the profile of the author
        of the pull reqest will be added to the issue line.

        :param str line: String containing a markdown-formatted single issue.
        :param dict issue: Fetched issue from GitHub.
        :rtype: str
        :return: Issue line with added author link.
        """
        if not issue.get("pull_request") or not self.options.author:
            return line

        if not issue.get("user"):
            line += u" (Null user)"
        elif self.options.username_as_tag:
            line += u" (@{0})".format(
                issue["user"]["login"]
            )
        else:
            line += u" ([{0}]({1}))".format(
                issue["user"]["login"], issue["user"]["html_url"]
            )
        return line