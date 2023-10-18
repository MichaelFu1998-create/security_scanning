def annotate_metadata_platform(repo):
    """
    Update metadata host information
    """

    print("Added platform information")
    package = repo.package
    mgr = plugins_get_mgr()
    repomgr = mgr.get(what='instrumentation', name='platform')
    package['platform'] = repomgr.get_metadata()