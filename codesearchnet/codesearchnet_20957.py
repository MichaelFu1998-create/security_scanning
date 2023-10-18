def _file_size(self, field):
        """ Returns the file size for given file field.

        Args:
            field (str): File field

        Returns:
            int. File size
        """
        size = 0
        try:
            handle = open(self._files[field], "r")
            size = os.fstat(handle.fileno()).st_size
            handle.close()
        except:
            size = 0
        self._file_lengths[field] = size
        return self._file_lengths[field]