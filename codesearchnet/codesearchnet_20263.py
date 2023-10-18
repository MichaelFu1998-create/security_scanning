def init(self, username, reponame, force, backend=None):
        """
        Initialize a Git repo

        Parameters
        ----------

        username, reponame : Repo name is tuple (name, reponame)
        force: force initialization of the repo even if exists
        backend: backend that must be used for this (e.g. s3)
        """
        key = self.key(username, reponame)

        # In local filesystem-based server, add a repo
        server_repodir = self.server_rootdir(username,
                                             reponame,
                                             create=False)

        # Force cleanup if needed
        if os.path.exists(server_repodir) and not force:
            raise RepositoryExists()

        if os.path.exists(server_repodir):
            shutil.rmtree(server_repodir)
        os.makedirs(server_repodir)

        # Initialize the repo
        with cd(server_repodir):
            git.init(".", "--bare")

        if backend is not None:
            backend.init_repo(server_repodir)

        # Now clone the filesystem-based repo
        repodir = self.rootdir(username, reponame, create=False)

        # Prepare it if needed
        if os.path.exists(repodir) and not force:
            raise Exception("Local repo already exists")
        if os.path.exists(repodir):
            shutil.rmtree(repodir)
        os.makedirs(repodir)

        # Now clone...
        with cd(os.path.dirname(repodir)):
            git.clone(server_repodir, '--no-hardlinks')

        url = server_repodir
        if backend is not None:
            url = backend.url(username, reponame)

        repo = Repo(username, reponame)
        repo.manager = self
        repo.remoteurl = url
        repo.rootdir = self.rootdir(username, reponame)

        self.add(repo)
        return repo