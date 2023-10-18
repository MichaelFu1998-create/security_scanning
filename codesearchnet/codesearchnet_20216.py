def lookup(username, reponame):
    """
    Lookup a repo based on username reponame
    """

    mgr = plugins_get_mgr()

    # XXX This should be generalized to all repo managers.
    repomgr = mgr.get(what='repomanager', name='git')
    repo =  repomgr.lookup(username=username,
                           reponame=reponame)
    return repo