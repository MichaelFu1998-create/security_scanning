def add_droplets(self, droplet_ids):
        """
        Assign a LoadBalancer to a Droplet.

        Args:
            droplet_ids (obj:`list` of `int`): A list of Droplet IDs
        """
        return self.get_data(
            "load_balancers/%s/droplets/" % self.id,
            type=POST,
            params={"droplet_ids": droplet_ids}
        )