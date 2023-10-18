def _validate_server(self):
        """Validates server information. Raises errors for required properties.
        """
        if not self._title:
            msg = "No 'title' in Server Discovery for request '{}'"
            raise ValidationError(msg.format(self.url))