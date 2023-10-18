def availableVersions(self):
        ''' return a list of GitCloneVersion objects for tags which are valid
            semantic version idenfitifiers.
        '''
        r = []
        for t in self.vcs.tags():
            logger.debug("available version tag: %s", t)
            # ignore empty tags:
            if not len(t.strip()):
                continue
            try:
                r.append(GitCloneVersion(t, t, self))
            except ValueError:
                logger.debug('invalid version tag: %s', t)
        return r