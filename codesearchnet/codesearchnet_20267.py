def permalink(self, repo, path):
        """
        Get the permalink to command that generated the dataset
        """

        if not os.path.exists(path): 
            # print("Path does not exist", path)
            return (None, None) 

        # Get this directory
        cwd = os.getcwd()

        # Find the root of the repo and cd into that directory..
        if os.path.isfile(path):
            os.chdir(os.path.dirname(path))

        rootdir = self._run(["rev-parse", "--show-toplevel"])
        if "fatal" in rootdir:
            # print("fatal", rootdir)
            return (None, None) 

        os.chdir(rootdir)
        # print("Rootdir = ", rootdir)

        # Now find relative path
        relpath = os.path.relpath(path, rootdir)
        # print("relpath = ", relpath)

        # Get the last commit for this file
        #3764cc2600b221ac7d7497de3d0dbcb4cffa2914
        sha1 = self._run(["log", "-n", "1", "--format=format:%H", relpath])
        # print("sha1 = ", sha1)

        # Get the repo URL
        #git@gitlab.com:pingali/simple-regression.git
        #https://gitlab.com/kanban_demo/test_project.git
        remoteurl = self._run(["config", "--get", "remote.origin.url"])
        # print("remoteurl = ", remoteurl)

        # Go back to the original directory...
        os.chdir(cwd)

        # Now match it against two possible formats of the remote url
        # Examples
        #https://help.github.com/articles/getting-permanent-links-to-files/
        #https://github.com/github/hubot/blob/ed25584f5ac2520a6c28547ffd0961c7abd7ea49/README.md
        #https://gitlab.com/pingali/simple-regression/blob/3764cc2600b221ac7d7497de3d0dbcb4cffa2914/model.py
        #https://github.com/pingali/dgit/blob/ff91b5d04b2978cad0bf9b006d1b0a16d18a778e/README.rst
        #https://gitlab.com/kanban_demo/test_project/blob/b004677c23b3a31eb7b5588a5194857b2c8b2b95/README.md

        m = re.search('^git@([^:\/]+):([^/]+)/([^/]+)', remoteurl)
        if m is None:
            m = re.search('^https://([^:/]+)/([^/]+)/([^/]+)', remoteurl)
        if m is not None:
            domain = m.group(1)
            username = m.group(2)
            project = m.group(3)
            if project.endswith(".git"):
                project = project[:-4]
            permalink = "https://{}/{}/{}/blob/{}/{}".format(domain, username, project,
                                                        sha1, relpath)
            # print("permalink = ", permalink)
            return (relpath, permalink)
        else:
            return (None, None)