def restore(self, image, wait=True):
        """
        Restore this droplet with given image id

        A Droplet restoration will rebuild an image using a backup image.
        The image ID that is passed in must be a backup of the current Droplet
        instance. The operation will leave any embedded SSH keys intact.

        Parameters
        ----------
        image: int or str
            int for image id and str for image slug
        wait: bool, default True
            Whether to block until the pending action is completed
        """
        return self._action('restore', image=image, wait=wait)