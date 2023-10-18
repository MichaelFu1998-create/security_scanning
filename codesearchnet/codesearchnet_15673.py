def to_cursor_ref(self):
        """Returns dict of values to uniquely reference this item"""
        fields = self._meta.get_primary_keys()
        assert fields
        values = {field.name:self.__data__[field.name] for field in fields}
        return values