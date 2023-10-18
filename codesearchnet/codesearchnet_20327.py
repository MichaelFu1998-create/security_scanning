def rebuild(self, image, wait=True):
        """
        Rebuild this droplet with given image id

        Parameters
        ----------
        image: int or str
            int for image id and str for image slug
        wait: bool, default True
            Whether to block until the pending action is completed
        """
        return self._action('rebuild', image=image, wait=wait)