def ensure_backrefs(obj, fields=None):
    """Ensure that all forward references on the provided object have the
    appropriate backreferences.

    :param StoredObject obj: Database record
    :param list fields: Optional list of field names to check

    """
    for ref in _collect_refs(obj, fields):
        updated = ref['value']._update_backref(
            ref['field_instance']._backref_field_name,
            obj,
            ref['field_name'],
        )
        if updated:
            logging.debug('Updated reference {}:{}:{}:{}:{}'.format(
                obj._name, obj._primary_key, ref['field_name'],
                ref['value']._name, ref['value']._primary_key,
            ))