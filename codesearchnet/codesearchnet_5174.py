def get_all_snapshots(self):
        """
            This method returns a list of all Snapshots.
        """
        data = self.get_data("snapshots/")
        return [
            Snapshot(token=self.token, **snapshot)
            for snapshot in data['snapshots']
        ]