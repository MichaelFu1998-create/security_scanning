def get_preferred_path(self):
        """Return preferred mapping for a resource mapping.

        Different URLs may map to the same resource, e.g.:
            '/a/b' == '/A/b' == '/a/b/'
        get_preferred_path() returns the same value for all these variants, e.g.:
            '/a/b/'   (assuming resource names considered case insensitive)

        @param path: a UTF-8 encoded, unquoted byte string.
        @return: a UTF-8 encoded, unquoted byte string.
        """
        if self.path in ("", "/"):
            return "/"
        # Append '/' for collections
        if self.is_collection and not self.path.endswith("/"):
            return self.path + "/"
        # TODO: handle case-sensitivity, depending on OS
        # (FileSystemProvider could do this with os.path:
        # (?) on unix we can assume that the path already matches exactly the case of filepath
        # on windows we could use path.lower() or get the real case from the
        # file system
        return self.path