def get_resource_inst(self, path, environ):
        """Return info dictionary for path.

        See get_resource_inst()
        """
        # TODO: calling exists() makes directory browsing VERY slow.
        #       At least compared to PyFileServer, which simply used string
        #       functions to get display_type and displayTypeComment
        self._count_get_resource_inst += 1
        if not self.exists(path, environ):
            return None
        _tableName, primKey = self._split_path(path)
        is_collection = primKey is None
        return MySQLBrowserResource(self, path, is_collection, environ)