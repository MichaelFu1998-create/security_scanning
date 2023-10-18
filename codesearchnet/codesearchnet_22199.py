def reload(self, *fields, **kwargs):
        """Reloads all attributes from the database.
        :param fields: (optional) args list of fields to reload
        :param max_depth: (optional) depth of dereferencing to follow
        .. versionadded:: 0.1.2
        .. versionchanged:: 0.6  Now chainable
        .. versionchanged:: 0.9  Can provide specific fields to reload
        """
        max_depth = 1
        if fields and isinstance(fields[0], int):
            max_depth = fields[0]
            fields = fields[1:]
        elif "max_depth" in kwargs:
            max_depth = kwargs["max_depth"]

        if not self.pk:
            raise self.DoesNotExist("Document does not exist")
        obj = self._qs.read_preference(ReadPreference.PRIMARY).filter(
            **self._object_key).only(*fields).limit(1
                                                    ).select_related(max_depth=max_depth)

        if obj:
            obj = obj[0]
        else:
            raise self.DoesNotExist("Document does not exist")

        for field in self._fields_ordered:
            if not fields or field in fields:
                try:
                    setattr(self, field, self._reload(field, obj[field]))
                except KeyError:
                    # If field is removed from the database while the object
                    # is in memory, a reload would cause a KeyError
                    # i.e. obj.update(unset__field=1) followed by obj.reload()
                    delattr(self, field)

        # BUG FIX BY US HERE:
        if not fields:
            self._changed_fields = obj._changed_fields
        else:
            for field in fields:
                field = self._db_field_map.get(field, field)
                if field in self._changed_fields:
                    self._changed_fields.remove(field)
        self._created = False
        return self