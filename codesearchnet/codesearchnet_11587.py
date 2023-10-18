def availableTags(self):
        ''' return a list of GithubComponentVersion objects for all tags
        '''
        return [
            GithubComponentVersion(
                '', t[0], t[1], self.name, cache_key=_createCacheKey('tag', t[0], t[1], self.name)
            ) for t in self._getTags()
        ]