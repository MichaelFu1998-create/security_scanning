def detect_actual_closed_dates(self, issues, kind):
        """
        Find correct closed dates, if issues was closed by commits.

        :param list issues: issues to check
        :param str kind: either "issues" or "pull requests"
        :rtype: list
        :return: issues with updated closed dates
        """

        if self.options.verbose:
            print("Fetching closed dates for {} {}...".format(
                len(issues), kind)
            )
        all_issues = copy.deepcopy(issues)
        for issue in all_issues:
            if self.options.verbose > 2:
                print(".", end="")
                if not issues.index(issue) % 30:
                    print("")
            self.find_closed_date_by_commit(issue)

            if not issue.get('actual_date', False):
                if issue.get('closed_at', False):
                    print("Skipping closed non-merged issue: #{0} {1}".format(
                        issue["number"], issue["title"]))

                all_issues.remove(issue)

        if self.options.verbose > 2:
            print(".")
        return all_issues