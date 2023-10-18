def _image_field(self):
        """
        Try to automatically detect an image field
        """
        for field in self.model._meta.fields:
            if isinstance(field, ImageField):
                return field.name