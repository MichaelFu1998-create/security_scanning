def remove_droplets(self, droplet_ids):
        """
        Unassign a LoadBalancer.

        Args:
            droplet_ids (obj:`list` of `int`): A list of Droplet IDs
        """
        return self.get_data(
            "load_balancers/%s/droplets/" % self.id,
            type=DELETE,
            params={"droplet_ids": droplet_ids}
        )