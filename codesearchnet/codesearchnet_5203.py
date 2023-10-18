def get_snapshots(self):
        """
        Retrieve the list of snapshots that have been created from a volume.

        Args:
        """
        data = self.get_data("volumes/%s/snapshots/" % self.id)
        snapshots = list()
        for jsond in data[u'snapshots']:
            snapshot = Snapshot(**jsond)
            snapshot.token = self.token
            snapshots.append(snapshot)

        return snapshots