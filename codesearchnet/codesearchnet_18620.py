def get_image(self, obj):
        """
        Return an ImageFileField instance
        """
        if self._meta.image_field:
            return getattr(obj, self._meta.image_field)