def ctime(self):
        """
        Get most recent create time in timestamp.
        """
        try:
            return self._stat.st_ctime
        except:  # pragma: no cover
            self._stat = self.stat()
            return self.ctime