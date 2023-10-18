def snapshot(self, name):
        """
        Create a snapshot of the volume.

        Args:
            name: string - a human-readable name for the snapshot
        """
        return self.get_data(
            "volumes/%s/snapshots/" % self.id,
            type=POST,
            params={"name": name}
        )