def _load_metadata(self, handle):
        """Load archive members metadata."""
        rarinfo = self._read_header(handle)
        while rarinfo:
            self.filelist.append(rarinfo)
            self.NameToInfo[rarinfo.filename] = rarinfo
            self._process_current(handle, constants.RAR_SKIP)
            rarinfo = self._read_header(handle)