def begin_write(self, content_type=None):
        """Open content as a stream for writing.

        See DAVResource.begin_write()
        """
        assert not self.is_collection
        self._check_write_access()
        mode = "wb"
        # GC issue 57: always store as binary
        #        if contentType and contentType.startswith("text"):
        #            mode = "w"
        return open(self.absFilePath, mode, BUFFER_SIZE)