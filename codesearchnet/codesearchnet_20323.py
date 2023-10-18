def get(self, id):
        """
        Retrieve a droplet by id

        Parameters
        ----------
        id: int
            droplet id

        Returns
        -------
        droplet: DropletActions
        """
        info = self._get_droplet_info(id)
        return DropletActions(self.api, self, **info)