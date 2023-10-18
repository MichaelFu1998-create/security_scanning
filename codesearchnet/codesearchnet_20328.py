def rename(self, name, wait=True):
        """
        Change the name of this droplet

        Parameters
        ----------
        name: str
            New name for the droplet
        wait: bool, default True
            Whether to block until the pending action is completed

        Raises
        ------
        APIError if region does not support private networking
        """
        return self._action('rename', name=name, wait=wait)