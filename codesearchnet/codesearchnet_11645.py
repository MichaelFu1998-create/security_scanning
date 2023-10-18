def commitVersion(self, spec):
        ''' return a GithubComponentVersion object for a specific commit if valid
        '''
        import re

        commit_match = re.match('^[a-f0-9]{7,40}$', spec, re.I)
        if commit_match:
            return GitCloneVersion('', spec, self)

        return None