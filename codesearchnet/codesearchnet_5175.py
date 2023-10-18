def get_droplet_snapshots(self):
        """
            This method returns a list of all Snapshots based on Droplets.
        """
        data = self.get_data("snapshots?resource_type=droplet")
        return [
            Snapshot(token=self.token, **snapshot)
            for snapshot in data['snapshots']
        ]