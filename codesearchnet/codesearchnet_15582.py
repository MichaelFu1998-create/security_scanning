def fetch_closed_pull_requests(self):
        """
        Fetch all pull requests. We need them to detect "merged_at" parameter

        :rtype: list
        :return: all pull requests
        """

        pull_requests = []
        verbose = self.options.verbose
        gh = self.github
        user = self.options.user
        repo = self.options.project
        if verbose:
            print("Fetching closed pull requests...")
        page = 1
        while page > 0:
            if verbose > 2:
                print(".", end="")

            if self.options.release_branch:
                rc, data = gh.repos[user][repo].pulls.get(
                    page=page, per_page=PER_PAGE_NUMBER, state='closed',
                    base=self.options.release_branch
                )
            else:
                rc, data = gh.repos[user][repo].pulls.get(
                    page=page, per_page=PER_PAGE_NUMBER, state='closed',
                )

            if rc == 200:
                pull_requests.extend(data)
            else:
                self.raise_GitHubError(rc, data, gh.getheaders())
            page = NextPage(gh)
        if verbose > 2:
            print(".")
        if verbose > 1:
            print("\tfetched {} closed pull requests.".format(
                len(pull_requests))
            )
        return pull_requests