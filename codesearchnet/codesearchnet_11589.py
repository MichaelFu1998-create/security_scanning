def commitVersion(self):
        ''' return a GithubComponentVersion object for a specific commit if valid
        '''
        import re

        commit_match = re.match('^[a-f0-9]{7,40}$', self.tagOrBranchSpec(), re.I)
        if commit_match:
            return GithubComponentVersion(
                '', '', _getCommitArchiveURL(self.repo, self.tagOrBranchSpec()), self.name, cache_key=None
            )

        return None