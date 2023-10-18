def _validate(self, value):
        """Validates a value as a proper Flow object.

        Args:
            value: A value to be set on the property.

        Raises:
            TypeError if the value is not an instance of Flow.
        """
        _LOGGER.info('validate: Got type %s', type(value))
        if value is not None and not isinstance(value, client.Flow):
            raise TypeError(
                'Property {0} must be convertible to a flow '
                'instance; received: {1}.'.format(self._name, value))