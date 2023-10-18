def iter_errors(self):
        """"Lazily yields each ValidationError for the received data dict.
        """

        # Deprecate
        warnings.warn(
            'Property "package.iter_errors" is deprecated.',
            UserWarning)

        return self.profile.iter_errors(self.to_dict())