def change_kernel(self, kernel_id, wait=True):
        """
        Change the kernel of this droplet

        Parameters
        ----------
        kernel_id: int
            Can be retrieved from output of self.kernels()
        wait: bool, default True
            Whether to block until the pending action is completed

        Raises
        ------
        APIError if region does not support private networking
        """
        return self._action('change_kernel', kernel=kernel_id, wait=wait)