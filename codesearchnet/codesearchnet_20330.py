def take_snapshot(self, name, wait=True):
        """
        Take a snapshot of this droplet (must be powered off)

        Parameters
        ----------
        name: str
            Name of the snapshot
        wait: bool, default True
            Whether to block until the pending action is completed
        """
        return self._action('snapshot', name=name, wait=wait)