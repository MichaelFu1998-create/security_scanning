def add(self, repo):
        """
        Add repo to the internal lookup table...
        """
        key = self.key(repo.username, repo.reponame)
        repo.key = key
        self.repos[key] = repo
        return key