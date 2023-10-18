def expand_resource_descriptor(descriptor):
    """Apply defaults to resource descriptor (IN-PLACE FOR NOW).
    """
    descriptor.setdefault('profile', config.DEFAULT_RESOURCE_PROFILE)
    if descriptor['profile'] == 'tabular-data-resource':

        # Schema
        schema = descriptor.get('schema')
        if schema is not None:
            for field in schema.get('fields', []):
                field.setdefault('type', config.DEFAULT_FIELD_TYPE)
                field.setdefault('format', config.DEFAULT_FIELD_FORMAT)
            schema.setdefault('missingValues', config.DEFAULT_MISSING_VALUES)

        # Dialect
        dialect = descriptor.get('dialect')
        if dialect is not None:
            for key, value in config.DEFAULT_DIALECT.items():
                dialect.setdefault(key, value)

    return descriptor