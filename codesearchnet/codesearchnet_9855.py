def _slugify_foreign_key(schema):
    """Slugify foreign key
    """
    for foreign_key in schema.get('foreignKeys', []):
        foreign_key['reference']['resource'] = _slugify_resource_name(
            foreign_key['reference'].get('resource', ''))
    return schema