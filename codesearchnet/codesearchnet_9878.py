def _convert_schemas(mapping, schemas):
    """Convert schemas to be compatible with storage schemas.

    Foreign keys related operations.

    Args:
        mapping (dict): mapping between resource name and table name
        schemas (list): schemas

    Raises:
        ValueError: if there is no resource
            for some foreign key in given mapping

    Returns:
        list: converted schemas

    """
    schemas = deepcopy(schemas)
    for schema in schemas:
        for fk in schema.get('foreignKeys', []):
            resource = fk['reference']['resource']
            if resource != 'self':
                if resource not in mapping:
                    message = 'Not resource "%s" for foreign key "%s"'
                    message = message % (resource, fk)
                    raise ValueError(message)
                fk['reference']['resource'] = mapping[resource]
    return schemas