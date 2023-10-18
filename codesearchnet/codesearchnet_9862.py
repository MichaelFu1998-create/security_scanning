def required_attributes(self):
        """tuple: The schema's required attributed.
        """

        # Deprecate
        warnings.warn(
            'Property "package.required_attributes" is deprecated.',
            UserWarning)
        required = ()

        # Get required
        try:
            if self.profile.required is not None:
                required = tuple(self.profile.required)
        except AttributeError:
            pass

        return required