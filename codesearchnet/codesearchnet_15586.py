def fetch_commit(self, event):
        """
        Fetch commit data for specified event.

        :param dict event: dictionary with event information
        :rtype: dict
        :return: dictionary with commit data
        """

        gh = self.github
        user = self.options.user
        repo = self.options.project

        rc, data = gh.repos[user][repo].git.commits[
            event["commit_id"]].get()
        if rc == 200:
            return data
        self.raise_GitHubError(rc, data, gh.getheaders())