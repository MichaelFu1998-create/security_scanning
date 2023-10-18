def size(self):
        """
        File size in bytes.
        """
        try:
            return self._stat.st_size
        except:  # pragma: no cover
            self._stat = self.stat()
            return self.size