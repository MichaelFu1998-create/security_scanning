def rootdir(self,  username, reponame, create=True):
        """
        Working directory for the repo
        """
        path = os.path.join(self.workspace,
                            'datasets',
                            username,
                            reponame)
        if create:
            try:
                os.makedirs(path)
            except:
                pass

        return path