def create_collection(self, name):
        """Create a new collection as member of self.

        A dummy member is created, because Mercurial doesn't handle folders.
        """
        assert self.is_collection
        self._check_write_access()
        collpath = self._getFilePath(name)
        os.mkdir(collpath)
        filepath = self._getFilePath(name, ".directory")
        f = open(filepath, "w")
        f.write("Created by WsgiDAV.")
        f.close()
        commands.add(self.provider.ui, self.provider.repo, filepath)