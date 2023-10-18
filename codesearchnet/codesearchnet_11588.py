def availableBranches(self):
        ''' return a list of GithubComponentVersion objects for the tip of each branch
        '''
        return [
            GithubComponentVersion(
                '', b[0], b[1], self.name, cache_key=None
            ) for b in _getBranchHeads(self.repo).items()
        ]