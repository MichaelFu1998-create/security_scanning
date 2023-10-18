def issues_to_log(self, issues, pull_requests):
        """
        Generate ready-to-paste log from list of issues and pull requests.

        :param list(dict) issues: List of issues in this tag section.
        :param list(dict) pull_requests: List of PR's in this tag section.
        :rtype: str
        :return: Generated log for issues and pull requests.
        """

        log = ""
        sections_a, issues_a = self.parse_by_sections(
            issues, pull_requests)

        for section, s_issues in sections_a.items():
            log += self.generate_sub_section(s_issues, section)
        log += self.generate_sub_section(issues_a, self.options.issue_prefix)
        return log