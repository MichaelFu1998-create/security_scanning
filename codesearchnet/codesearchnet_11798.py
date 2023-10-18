def local_renderer(self):
        """
        Retrieves the cached local renderer.
        """
        if not self._local_renderer:
            r = self.create_local_renderer()
            self._local_renderer = r
        return self._local_renderer