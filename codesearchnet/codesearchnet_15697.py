def _validate_collection(self):
        """Validates Collection information. Raises errors for required
        properties."""
        if not self._id:
            msg = "No 'id' in Collection for request '{}'"
            raise ValidationError(msg.format(self.url))

        if not self._title:
            msg = "No 'title' in Collection for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self._can_read is None:
            msg = "No 'can_read' in Collection for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self._can_write is None:
            msg = "No 'can_write' in Collection for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self._id not in self.url:
            msg = "The collection '{}' does not match the url for queries '{}'"
            raise ValidationError(msg.format(self._id, self.url))