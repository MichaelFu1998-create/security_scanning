def fetch_repo_creation_date(self):
        """
        Get the creation date of the repository from GitHub.

        :rtype: str, str
        :return: special tag name, creation date as ISO date string
        """
        gh = self.github
        user = self.options.user
        repo = self.options.project
        rc, data = gh.repos[user][repo].get()
        if rc == 200:
            return REPO_CREATED_TAG_NAME, data["created_at"]
        else:
            self.raise_GitHubError(rc, data, gh.getheaders())
        return None, None