def resize(self, size_gigabytes, region):
        """
        Detach a Volume to a Droplet.

        Args:
            size_gigabytes: int - size of the Block Storage volume in GiB
            region: string - slug identifier for the region
        """
        return self.get_data(
            "volumes/%s/actions/" % self.id,
            type=POST,
            params={"type": "resize",
                    "size_gigabytes": size_gigabytes,
                    "region": region}
        )