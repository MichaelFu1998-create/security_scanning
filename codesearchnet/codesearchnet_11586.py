def availableVersions(self):
        ''' return a list of Version objects, each with a tarball URL set '''
        r = []
        for t in self._getTags():
            logger.debug("available version tag: %s", t)
            # ignore empty tags:
            if not len(t[0].strip()):
                continue
            try:
                r.append(GithubComponentVersion(t[0], t[0], url=t[1], name=self.name, cache_key=None))
            except ValueError:
                logger.debug('invalid version tag: %s', t)

        return r