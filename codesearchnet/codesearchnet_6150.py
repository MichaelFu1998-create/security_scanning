def get_member(self, name):
        """Return direct collection member (DAVResource or derived).

        See DAVCollection.get_member()
        """
        assert compat.is_native(name), "{!r}".format(name)
        fp = os.path.join(self._file_path, compat.to_unicode(name))
        #        name = name.encode("utf8")
        path = util.join_uri(self.path, name)
        if os.path.isdir(fp):
            res = FolderResource(path, self.environ, fp)
        elif os.path.isfile(fp):
            res = FileResource(path, self.environ, fp)
        else:
            _logger.debug("Skipping non-file {}".format(path))
            res = None
        return res