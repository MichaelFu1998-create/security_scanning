def drop(self, repo, args=[]):
        """
        Cleanup the repo
        """

        # Clean up the rootdir
        rootdir = repo.rootdir
        if os.path.exists(rootdir):
            print("Cleaning repo directory: {}".format(rootdir))
            shutil.rmtree(rootdir)

        # Cleanup the local version of the repo (this could be on
        # the server etc.
        server_repodir = self.server_rootdir_from_repo(repo,
                                                       create=False)
        if os.path.exists(server_repodir):
            print("Cleaning data from local git 'server': {}".format(server_repodir))
            shutil.rmtree(server_repodir)

        super(GitRepoManager, self).drop(repo)

        return {
            'status': 'success',
            'message': "successful cleanup"
        }