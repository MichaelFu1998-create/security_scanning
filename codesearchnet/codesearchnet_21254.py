def path(self):
        """
        Return the path always without the \\?\ prefix.
        """
        path = super(WindowsPath2, self).path
        if path.startswith("\\\\?\\"):
            return path[4:]
        return path