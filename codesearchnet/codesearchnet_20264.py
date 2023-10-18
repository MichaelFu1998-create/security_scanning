def clone(self, url, backend=None):
        """
        Clone a URL

        Parameters
        ----------

        url : URL of the repo. Supports s3://, git@, http://
        """


        # s3://bucket/git/username/repo.git
        username = self.username
        reponame = url.split("/")[-1] # with git
        reponame = reponame.replace(".git","")

        key = (username, reponame)

        # In local filesystem-based server, add a repo
        server_repodir = self.server_rootdir(username,
                                             reponame,
                                             create=False)

        rootdir = self.rootdir(username,  reponame, create=False)


        if backend is None:
            # Backend is standard git repo (https://, git@...)
            with cd(os.path.dirname(rootdir)):
                self._run(['clone', '--no-hardlinks', url])
        else:
            # Backend is s3
            # Sync if needed.
            if not os.path.exists(server_repodir):
                # s3 -> .dgit/git/pingali/hello.git -> .dgit/datasets/pingali/hello
                backend.clone_repo(url, server_repodir)

            # After sync clone,
            with cd(os.path.dirname(rootdir)):
                self._run(['clone', '--no-hardlinks', server_repodir])


        # Insert the notes push
        if True:
            configfile = os.path.join(rootdir, '.git', 'config')
            content = open(configfile).read()
            original = "fetch = +refs/heads/*:refs/remotes/origin/*"
            replacement ="""fetch = +refs/heads/*:refs/remotes/origin/*\n        fetch = +refs/notes/*:refs/notes/*"""
            if "notes" not in content:
                content = content.replace(original, replacement)
                with open(configfile, 'w') as fd:
                    fd.write(content)

            # Pull the notes if any as well..
            with cd(rootdir):
                self._run(['pull','origin'])

        # Insert the object into the internal table we maintain...
        r = Repo(username, reponame)
        r.rootdir = rootdir
        r.remoteurl = url
        r.manager = self

        package = os.path.join(r.rootdir, 'datapackage.json')
        packagedata = open(package).read()
        r.package = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(packagedata)

        return self.add(r)