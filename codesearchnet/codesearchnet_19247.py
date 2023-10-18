def _validate_schema(obj):
    """Ensures the passed schema instance is compatible

    :param obj: object to validate
    :return: obj
    :raises:
        - IncompatibleSchema if the passed schema is of an incompatible type
    """

    if obj is not None and not isinstance(obj, Schema):
        raise IncompatibleSchema('Schema must be of type {0}'.format(Schema))

    return obj