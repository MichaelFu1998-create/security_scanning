def _prepare_edit(self, record):
        """Update selected keys.

        :param record: The record to prepare.
        """
        data = record.dumps()
        # Keep current record revision for merging.
        data['_deposit']['pid']['revision_id'] = record.revision_id
        data['_deposit']['status'] = 'draft'
        data['$schema'] = self.build_deposit_schema(record)
        return data