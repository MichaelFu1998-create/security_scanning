def extended_path(self):
        """
        Add prefix \\?\ to every absolute path, so that it's a "extended-length"
        path, that should be longer than 259 characters (called: "MAX_PATH")
        see:
        https://msdn.microsoft.com/en-us/library/aa365247.aspx#maxpath
        """
        if self.is_absolute() and not self.path.startswith("\\\\"):
            return "\\\\?\\%s" % self.path
        return self.path