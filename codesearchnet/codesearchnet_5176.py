def get_volume_snapshots(self):
        """
            This method returns a list of all Snapshots based on volumes.
        """
        data = self.get_data("snapshots?resource_type=volume")
        return [
            Snapshot(token=self.token, **snapshot)
            for snapshot in data['snapshots']
        ]