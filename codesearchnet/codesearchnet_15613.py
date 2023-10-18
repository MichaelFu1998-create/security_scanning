def parse_by_sections(self, issues, pull_requests):
        """
        This method sort issues by types (bugs, features, etc. or
        just closed issues) by labels.

        :param list(dict) issues: List of issues in this tag section.
        :param list(dict) pull_requests: List of PR's in this tag section.
        :rtype: dict(list(dict)), list(dict)
        :return: Issues and PR's sorted into sections.
        """

        issues_a = []
        sections_a = OrderedDict()

        if not self.options.sections:
            return [sections_a, issues]
        for key in self.options.sections:
            sections_a.update({key: []})
        self.parse_by_sections_for_issues(issues, sections_a, issues_a)
        self.parse_by_sections_for_pr(pull_requests, sections_a)
        return [sections_a, issues_a]