def serialize(self):
        """All concrete fields of the ``SyncableModel`` subclass, except for those specifically blacklisted, are returned in a dict."""
        # NOTE: code adapted from https://github.com/django/django/blob/master/django/forms/models.py#L75
        opts = self._meta

        data = {}
        for f in opts.concrete_fields:
            if f.attname in self.morango_fields_not_to_serialize:
                continue
            if f.attname in self._morango_internal_fields_not_to_serialize:
                continue
            # case if model is morango mptt
            if f.attname in getattr(self, '_internal_mptt_fields_not_to_serialize', '_internal_fields_not_to_serialize'):
                continue
            if hasattr(f, 'value_from_object_json_compatible'):
                data[f.attname] = f.value_from_object_json_compatible(self)
            else:
                data[f.attname] = f.value_from_object(self)
        return data