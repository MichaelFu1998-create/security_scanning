def resize(self, size, wait=True):
        """
        Change the size of this droplet (must be powered off)

        Parameters
        ----------
        size: str
            size slug, e.g., 512mb
        wait: bool, default True
            Whether to block until the pending action is completed
        """
        return self._action('resize', size=size, wait=wait)