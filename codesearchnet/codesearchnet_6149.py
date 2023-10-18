def get_member_names(self):
        """Return list of direct collection member names (utf-8 encoded).

        See DAVCollection.get_member_names()
        """
        # On Windows NT/2k/XP and Unix, if path is a Unicode object, the result
        # will be a list of Unicode objects.
        # Undecodable filenames will still be returned as string objects
        # If we don't request unicode, for example Vista may return a '?'
        # instead of a special character. The name would then be unusable to
        # build a distinct URL that references this resource.

        nameList = []
        # self._file_path is unicode, so os.listdir returns unicode as well
        assert compat.is_unicode(self._file_path)
        for name in os.listdir(self._file_path):
            if not compat.is_unicode(name):
                name = name.decode(sys.getfilesystemencoding())
            assert compat.is_unicode(name)
            # Skip non files (links and mount points)
            fp = os.path.join(self._file_path, name)
            if not os.path.isdir(fp) and not os.path.isfile(fp):
                _logger.debug("Skipping non-file {!r}".format(fp))
                continue
            # name = name.encode("utf8")
            name = compat.to_native(name)
            nameList.append(name)
        return nameList