def clone(url):
    """
    Clone a URL. Examples include:

        - git@github.com:pingali/dgit.git
        - https://github.com:pingali/dgit.git
        - s3://mybucket/git/pingali/dgit.git

    Parameters
    ----------

    url: URL of the repo

    """
    backend = None
    backendmgr = None
    if url.startswith('s3'):
        backendtype = 's3'
    elif url.startswith("http") or url.startswith("git"):
        backendtype = 'git'
    else:
        backendtype = None

    mgr = plugins_get_mgr()
    repomgr = mgr.get(what='repomanager', name='git')
    backendmgr = mgr.get(what='backend', name=backendtype)

    # print("Testing {} with backend {}".format(url, backendmgr))
    if backendmgr is not None and not backendmgr.url_is_valid(url):
        raise InvalidParameters("Invalid URL")

    key = repomgr.clone(url, backendmgr)

    # Insert a datapackage if it doesnt already exist...
    repo = repomgr.lookup(key=key)
    if not datapackage_exists(repo):
        filename = bootstrap_datapackage(repo)
        repo.run('add_files',
                 [
                     {
                         'relativepath': 'datapackage.json',
                         'localfullpath': filename,
                    },
                 ])
        os.unlink(filename)
        args = ['-a', '-m', 'Bootstrapped the repo']
        repo.run('commit', args)

    return repo