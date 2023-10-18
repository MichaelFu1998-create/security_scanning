def begin_write(self, content_type=None):
        """Open content as a stream for writing.

        See DAVResource.begin_write()
        """
        assert not self.is_collection
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        # _logger.debug("begin_write: {}, {}".format(self._file_path, "wb"))
        # GC issue 57: always store as binary
        return open(self._file_path, "wb", BUFFER_SIZE)