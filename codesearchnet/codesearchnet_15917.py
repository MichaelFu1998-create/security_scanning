def getinfo(self, name):
        """Return the instance of RarInfo given 'name'."""
        rarinfo = self.NameToInfo.get(name)
        if rarinfo is None:
            raise KeyError('There is no item named %r in the archive' % name)
        return rarinfo