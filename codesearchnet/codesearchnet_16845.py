def _publish_new(self, id_=None):
        """Publish new deposit.

        :param id_: The forced record UUID.
        """
        minter = current_pidstore.minters[
            current_app.config['DEPOSIT_PID_MINTER']
        ]
        id_ = id_ or uuid.uuid4()
        record_pid = minter(id_, self)

        self['_deposit']['pid'] = {
            'type': record_pid.pid_type,
            'value': record_pid.pid_value,
            'revision_id': 0,
        }

        data = dict(self.dumps())
        data['$schema'] = self.record_schema

        with self._process_files(id_, data):
            record = self.published_record_class.create(data, id_=id_)

        return record