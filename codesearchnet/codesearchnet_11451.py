def add_issues(self, issues):
        """
        Adds an issue to the collection.

        :param issues: the issue(s) to add
        :type issues: tidypy.Issue or list(tidypy.Issue)
        """

        if not isinstance(issues, (list, tuple)):
            issues = [issues]
        with self._lock:
            self._all_issues.extend(issues)
            self._cleaned_issues = None