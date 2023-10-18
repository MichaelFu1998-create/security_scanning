def attributes(self):
        """tuple: Attributes defined in the schema and the data package.
        """

        # Deprecate
        warnings.warn(
            'Property "package.attributes" is deprecated.',
            UserWarning)

        # Get attributes
        attributes = set(self.to_dict().keys())
        try:
            attributes.update(self.profile.properties.keys())
        except AttributeError:
            pass

        return tuple(attributes)