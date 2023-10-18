def extract(self, member, path=None, pwd=None):
        """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. `member' may be a filename or a RarInfo object. You can
           specify a different directory using `path'.
        """
        if isinstance(member, RarInfo):
            member = member.filename

        if path is None:
            path = os.getcwd()

        self._extract_members([member], path, pwd)
        return os.path.join(path, member)