def process_schema(value):
    """Load schema from JSONSchema registry based on given value.

    :param value: Schema path, relative to the directory when it was
        registered.
    :returns: The schema absolute path.
    """
    schemas = current_app.extensions['invenio-jsonschemas'].schemas
    try:
        return schemas[value]
    except KeyError:
        raise click.BadParameter(
            'Unknown schema {0}. Please use one of:\n {1}'.format(
                value, '\n'.join(schemas.keys())
            )
        )