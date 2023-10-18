def is_collection(self, path, environ):
        """Return True, if path maps to an existing collection resource.

        This method should only be used, if no other information is queried
        for <path>. Otherwise a _DAVResource should be created first.
        """
        res = self.get_resource_inst(path, environ)
        return res and res.is_collection