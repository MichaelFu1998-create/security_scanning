def get_snapshot(self, snapshot_id):
        """
            Return a Snapshot by its ID.
        """
        return Snapshot.get_object(
            api_token=self.token, snapshot_id=snapshot_id
        )