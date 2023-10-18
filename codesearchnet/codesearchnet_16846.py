def _publish_edited(self):
        """Publish the deposit after for editing."""
        record_pid, record = self.fetch_published()
        if record.revision_id == self['_deposit']['pid']['revision_id']:
            data = dict(self.dumps())
        else:
            data = self.merge_with_published()

        data['$schema'] = self.record_schema
        data['_deposit'] = self['_deposit']
        record = record.__class__(data, model=record.model)
        return record