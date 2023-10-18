def _getTags(repo):
    ''' return a dictionary of {tag: tarball_url}'''
    logger.debug('get tags for %s', repo)
    g = Github(settings.getProperty('github', 'authtoken'))
    repo = g.get_repo(repo)
    tags = repo.get_tags()
    logger.debug('tags for %s: %s', repo, [t.name for t in tags])
    return {t.name: _ensureDomainPrefixed(t.tarball_url) for t in tags}