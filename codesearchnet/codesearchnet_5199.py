def create_from_snapshot(self, *args, **kwargs):
        """
        Creates a Block Storage volume

        Note: Every argument and parameter given to this method will be
        assigned to the object.

        Args:
            name: string - a name for the volume
            snapshot_id: string - unique identifier for the volume snapshot
            size_gigabytes: int - size of the Block Storage volume in GiB
            filesystem_type: string, optional - name of the filesystem type the
                volume will be formated with ('ext4' or 'xfs')
            filesystem_label: string, optional - the label to be applied to the
                filesystem, only used in conjunction with filesystem_type

        Optional Args:
            description: string - text field to describe a volume
        """
        data = self.get_data('volumes/',
                             type=POST,
                             params={'name': self.name,
                                     'snapshot_id': self.snapshot_id,
                                     'region': self.region,
                                     'size_gigabytes': self.size_gigabytes,
                                     'description': self.description,
                                     'filesystem_type': self.filesystem_type,
                                     'filesystem_label': self.filesystem_label
                                     })

        if data:
            self.id = data['volume']['id']
            self.created_at = data['volume']['created_at']

        return self