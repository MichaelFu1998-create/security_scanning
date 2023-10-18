def atime(self):
        """
        Get most recent access time in timestamp.
        """
        try:
            return self._stat.st_atime
        except:  # pragma: no cover
            self._stat = self.stat()
            return self.atime