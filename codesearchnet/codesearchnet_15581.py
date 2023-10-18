def fetch_closed_issues_and_pr(self):
        """
        This method fetches all closed issues and separate them to
        pull requests and pure issues (pull request is kind of issue
        in term of GitHub).

        :rtype: list, list
        :return: issues, pull-requests
        """

        verbose = self.options.verbose
        gh = self.github
        user = self.options.user
        repo = self.options.project
        if verbose:
            print("Fetching closed issues and pull requests...")

        data = []
        issues = []
        data = []
        page = 1
        while page > 0:
            if verbose > 2:
                print(".", end="")
            rc, data = gh.repos[user][repo].issues.get(
                page=page, per_page=PER_PAGE_NUMBER,
                state='closed', filter='all'
            )
            if rc == 200:
                issues.extend(data)
            else:
                self.raise_GitHubError(rc, data, gh.getheaders())
            if len(issues) >= self.options.max_issues:
                break
            page = NextPage(gh)
        self.first_issue = data[-1] if len(data) > 0 else []
        if verbose > 2:
            print(".")

        # separate arrays of issues and pull requests:
        prs = []
        iss = []
        for i in issues:
            if "pull_request" in i:
                prs.append(i)
            else:
                iss.append(i)
        if verbose > 1:
            print("\treceived {} issues and  {} pull requests.".format(
                len(iss), len(prs))
            )
        return iss, prs