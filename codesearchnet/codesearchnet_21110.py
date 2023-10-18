def filelist(self):
        """
        Return list of files in filetree.
        """
        if len(self._filelist) == 0:
            for item in self._data:
                if isinstance(self._data[item], filetree):
                    self._filelist.extend(self._data[item].filelist())
                else:
                    self._filelist.append(self._data[item])
        return self._filelist