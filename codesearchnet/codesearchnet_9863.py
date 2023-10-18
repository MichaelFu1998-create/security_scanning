def validate(self):
        """"Validate this Data Package.
        """

        # Deprecate
        warnings.warn(
            'Property "package.validate" is deprecated.',
            UserWarning)

        descriptor = self.to_dict()
        self.profile.validate(descriptor)