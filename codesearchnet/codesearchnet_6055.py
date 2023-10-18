def _split_path(self, path):
        """Return (tableName, primaryKey) tuple for a request path."""
        if path.strip() in (None, "", "/"):
            return (None, None)
        tableName, primKey = util.save_split(path.strip("/"), "/", 1)
        #        _logger.debug("'%s' -> ('%s', '%s')" % (path, tableName, primKey))
        return (tableName, primKey)