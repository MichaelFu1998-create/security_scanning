def delete(self, wait=True):
        """
        Delete this droplet

        Parameters
        ----------
        wait: bool, default True
            Whether to block until the pending action is completed
        """
        resp = self.parent.delete(self.id)
        if wait:
            self.wait()
        return resp