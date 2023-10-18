def get_all_tags(self):
        """
        Fetch all tags for repository from Github.

        :return: tags in repository
        :rtype: list
        """

        verbose = self.options.verbose
        gh = self.github
        user = self.options.user
        repo = self.options.project
        if verbose:
            print("Fetching tags...")

        tags = []
        page = 1
        while page > 0:
            if verbose > 2:
                print(".", end="")
            rc, data = gh.repos[user][repo].tags.get(
                page=page, per_page=PER_PAGE_NUMBER)
            if rc == 200:
                tags.extend(data)
            else:
                self.raise_GitHubError(rc, data, gh.getheaders())
            page = NextPage(gh)
        if verbose > 2:
            print(".")

        if len(tags) == 0:
            if not self.options.quiet:
                print("Warning: Can't find any tags in repo. Make sure, that "
                      "you push tags to remote repo via 'git push --tags'")
                exit()
        if verbose > 1:
            print("Found {} tag(s)".format(len(tags)))
        return tags