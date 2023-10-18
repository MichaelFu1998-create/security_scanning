def run(self, cmd, *args):
        """
        Run a specific command using the manager
        """
        if self.manager is None:
            raise Exception("Fatal internal error: Missing repository manager")
        if cmd not in dir(self.manager):
            raise Exception("Fatal internal error: Invalid command {} being run".format(cmd))
        func = getattr(self.manager, cmd)
        repo = self
        return func(repo, *args)