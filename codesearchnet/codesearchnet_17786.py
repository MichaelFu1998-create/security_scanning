def get_default_fields(self):
        """
        get all fields of model, execpt id
        """
        field_names = self._meta.get_all_field_names()
        if 'id' in field_names:
            field_names.remove('id')

        return field_names