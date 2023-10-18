def edit(self, pid=None):
        """Edit deposit.

        #. The signal :data:`invenio_records.signals.before_record_update`
           is sent before the edit execution.

        #. The following meta information are saved inside the deposit:

        .. code-block:: python

            deposit['_deposit']['pid'] = record.revision_id
            deposit['_deposit']['status'] = 'draft'
            deposit['$schema'] = deposit_schema_from_record_schema

        #. The signal :data:`invenio_records.signals.after_record_update` is
            sent after the edit execution.

        #. The deposit index is updated.

        Status required: `published`.

        .. note:: the process fails if the pid has status
            :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`.

        :param pid: Force a pid object. (Default: ``None``)
        :returns: A new Deposit object.
        """
        pid = pid or self.pid

        with db.session.begin_nested():
            before_record_update.send(
                current_app._get_current_object(), record=self)

            record_pid, record = self.fetch_published()
            assert PIDStatus.REGISTERED == record_pid.status
            assert record['_deposit'] == self['_deposit']

            self.model.json = self._prepare_edit(record)

            flag_modified(self.model, 'json')
            db.session.merge(self.model)

        after_record_update.send(
            current_app._get_current_object(), record=self)
        return self.__class__(self.model.json, model=self.model)