def fetch_date_of_tag(self, tag):
        """
        Fetch time for tag from repository.

        :param dict tag: dictionary with tag information
        :rtype: str
        :return: time of specified tag as ISO date string
        """

        if self.options.verbose > 1:
            print("\tFetching date for tag {}".format(tag["name"]))
        gh = self.github
        user = self.options.user
        repo = self.options.project

        rc, data = gh.repos[user][repo].git.commits[
            tag["commit"]["sha"]].get()
        if rc == 200:
            return data["committer"]["date"]
        self.raise_GitHubError(rc, data, gh.getheaders())