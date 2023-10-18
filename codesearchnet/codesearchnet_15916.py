def namelist(self):
        """Return a list of file names in the archive."""
        names = []
        for member in self.filelist:
            names.append(member.filename)
        return names