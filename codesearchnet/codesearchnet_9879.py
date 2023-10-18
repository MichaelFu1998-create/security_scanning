def _restore_resources(resources):
    """Restore schemas from being compatible with storage schemas.

    Foreign keys related operations.

    Args:
        list: resources from storage

    Returns:
        list: restored resources

    """
    resources = deepcopy(resources)
    for resource in resources:
        schema = resource['schema']
        for fk in schema.get('foreignKeys', []):
            _, name = _restore_path(fk['reference']['resource'])
            fk['reference']['resource'] = name
    return resources