def get_string_for_issue(self, issue):
        """
        Parse issue and generate single line formatted issue line.

        Example output:
            - Add coveralls integration [\#223](https://github.com/skywinder/github-changelog-generator/pull/223) ([skywinder](https://github.com/skywinder))
            - Add coveralls integration [\#223](https://github.com/skywinder/github-changelog-generator/pull/223) (@skywinder)


        :param dict issue: Fetched issue from GitHub.
        :rtype: str
        :return: Markdown-formatted single issue.
        """

        encapsulated_title = self.encapsulate_string(issue['title'])
        try:
            title_with_number = u"{0} [\\#{1}]({2})".format(
                encapsulated_title, issue["number"], issue["html_url"]
            )
        except UnicodeEncodeError:
            # TODO: why did i add this? Is it needed?
            title_with_number = "ERROR ERROR ERROR: #{0} {1}".format(
                issue["number"], issue['title']
            )
            print(title_with_number, '\n', issue["html_url"])
        return self.issue_line_with_user(title_with_number, issue)