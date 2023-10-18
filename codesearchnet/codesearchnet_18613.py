def _date_field(self):
        """
        Try to automatically detect an image field
        """
        for field in self.model._meta.fields:
            if isinstance(field, (DateTimeField, DateField)):
                return field.name