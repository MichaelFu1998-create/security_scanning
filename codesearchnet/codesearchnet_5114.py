def get_object(cls, api_token, snapshot_id):
        """
            Class method that will return a Snapshot object by ID.
        """
        snapshot = cls(token=api_token, id=snapshot_id)
        snapshot.load()
        return snapshot