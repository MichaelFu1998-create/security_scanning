def assign(self, droplet_id):
        """
            Assign a FloatingIP to a Droplet.

            Args:
                droplet_id: int - droplet id
        """
        return self.get_data(
            "floating_ips/%s/actions/" % self.ip,
            type=POST,
            params={"type": "assign", "droplet_id": droplet_id}
        )