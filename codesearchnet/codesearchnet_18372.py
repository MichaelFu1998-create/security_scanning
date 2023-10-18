def mtime(self):
        """
        Get most recent modify time in timestamp.
        """
        try:
            return self._stat.st_mtime
        except:  # pragma: no cover
            self._stat = self.stat()
            return self.mtime