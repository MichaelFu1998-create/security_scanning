def _validate_api_root(self):
        """Validates API Root information. Raises errors for required
        properties."""
        if not self._title:
            msg = "No 'title' in API Root for request '{}'"
            raise ValidationError(msg.format(self.url))

        if not self._versions:
            msg = "No 'versions' in API Root for request '{}'"
            raise ValidationError(msg.format(self.url))

        if self._max_content_length is None:
            msg = "No 'max_content_length' in API Root for request '{}'"
            raise ValidationError(msg.format(self.url))