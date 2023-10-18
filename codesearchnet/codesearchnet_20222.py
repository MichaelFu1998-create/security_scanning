def init(username, reponame, setup,
         force=False, options=None,
         noinput=False):
    """
    Initialize an empty repository with datapackage.json

    Parameters
    ----------

    username: Name of the user
    reponame: Name of the repo
    setup: Specify the 'configuration' (git only, git+s3 backend etc)
    force: Force creation of the files
    options: Dictionary with content of dgit.json, if available.
    noinput: Automatic operation with no human interaction
    """

    mgr = plugins_get_mgr()
    repomgr = mgr.get(what='repomanager', name='git')

    backendmgr = None
    if setup == 'git+s3':
        backendmgr = mgr.get(what='backend', name='s3')

    repo = repomgr.init(username, reponame, force, backendmgr)

    # Now bootstrap the datapackage.json metadata file and copy it in...

    # Insert a gitignore with .dgit directory in the repo. This
    # directory will be used to store partial results
    (handle, gitignore) = tempfile.mkstemp()
    with open(gitignore, 'w') as fd:
        fd.write(".dgit")

    # Try to bootstrap. If you cant, cleanup and return
    try:
        filename = bootstrap_datapackage(repo, force, options, noinput)
    except Exception as e:
        repomgr.drop(repo,[])
        os.unlink(gitignore)
        raise e

    repo.run('add_files',
             [
                 {
                     'relativepath': 'datapackage.json',
                     'localfullpath': filename,
                 },
                 {
                     'relativepath': '.gitignore',
                     'localfullpath': gitignore,
                 },
             ])


    # Cleanup temp files
    os.unlink(filename)
    os.unlink(gitignore)

    args = ['-a', '-m', 'Bootstrapped the repo']
    repo.run('commit', args)
    
    return repo