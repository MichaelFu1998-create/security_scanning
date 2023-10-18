def clone(self):
        """
        Returns a copy of this object
        """
        t = Tag(self.version.major, self.version.minor, self.version.patch)
        if self.revision is not None:
            t.revision = self.revision.clone()
        return t