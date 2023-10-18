def iter_errors(self, data):
        """Lazily yields each ValidationError for the received data dict.
        """

        # Deprecate
        warnings.warn(
            'Property "profile.iter_errors" is deprecated.',
            UserWarning)

        for error in self._validator.iter_errors(data):
            yield error