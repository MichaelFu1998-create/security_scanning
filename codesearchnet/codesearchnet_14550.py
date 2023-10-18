def restore_snapshot(self, datacenter_id, volume_id, snapshot_id):
        """
        Restores a snapshot to the specified volume.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """
        data = {'snapshotId': snapshot_id}

        response = self._perform_request(
            url='/datacenters/%s/volumes/%s/restore-snapshot' % (
                datacenter_id,
                volume_id),
            method='POST-ACTION',
            data=urlencode(data))

        return response