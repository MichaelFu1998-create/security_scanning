def list_repos(remote=False):
    """
    List repos

    Parameters
    ----------

    remote: Flag
    """
    mgr = plugins_get_mgr()

    if not remote:
        repomgr = mgr.get(what='repomanager', name='git')
        repos = repomgr.get_repo_list()
        repos.sort()
        return repos
    else:
        raise Exception("Not supported yet")