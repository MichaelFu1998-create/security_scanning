def attach(self, droplet_id, region):
        """
        Attach a Volume to a Droplet.

        Args:
            droplet_id: int - droplet id
            region: string - slug identifier for the region
        """
        return self.get_data(
            "volumes/%s/actions/" % self.id,
            type=POST,
            params={"type": "attach",
                    "droplet_id": droplet_id,
                    "region": region}
        )