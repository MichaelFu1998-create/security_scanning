def auto_get_repo(autooptions, debug=False):
    """
    Automatically get repo

    Parameters
    ----------

    autooptions: dgit.json content

    """

    # plugin manager
    pluginmgr = plugins_get_mgr()

    # get the repo manager
    repomgr = pluginmgr.get(what='repomanager', name='git')

    repo = None

    try:
        if debug:
            print("Looking repo")
        repo = repomgr.lookup(username=autooptions['username'],
                              reponame=autooptions['reponame'])
    except:
        # Clone the repo
        try:
            print("Checking and cloning if the dataset exists on backend")
            url = autooptions['remoteurl']
            if debug:
                print("Doesnt exist. trying to clone: {}".format(url))
            common_clone(url)
            repo = repomgr.lookup(username=autooptions['username'],
                                  reponame=autooptions['reponame'])
            if debug:
                print("Cloning successful")
        except:
            # traceback.print_exc()
            yes = input("Repo doesnt exist. Should I create one? [yN]")
            if yes == 'y':
                setup = "git"
                if autooptions['remoteurl'].startswith('s3://'):
                    setup = 'git+s3'
                repo = common_init(username=autooptions['username'],
                                   reponame=autooptions['reponame'],
                                   setup=setup,
                                   force=True,
                                   options=autooptions)

                if debug:
                    print("Successfully inited repo")
            else:
                raise Exception("Cannot load repo")

    repo.options = autooptions

    return repo