def discard(self, pid=None):
        """Discard deposit changes.

        #. The signal :data:`invenio_records.signals.before_record_update` is
            sent before the edit execution.

        #. It restores the last published version.

        #. The following meta information are saved inside the deposit:

        .. code-block:: python

            deposit['$schema'] = deposit_schema_from_record_schema

        #. The signal :data:`invenio_records.signals.after_record_update` is
            sent after the edit execution.

        #. The deposit index is updated.

        Status required: ``'draft'``.

        :param pid: Force a pid object. (Default: ``None``)
        :returns: A new Deposit object.
        """
        pid = pid or self.pid

        with db.session.begin_nested():
            before_record_update.send(
                current_app._get_current_object(), record=self)

            _, record = self.fetch_published()
            self.model.json = deepcopy(record.model.json)
            self.model.json['$schema'] = self.build_deposit_schema(record)

            flag_modified(self.model, 'json')
            db.session.merge(self.model)

        after_record_update.send(
            current_app._get_current_object(), record=self)
        return self.__class__(self.model.json, model=self.model)