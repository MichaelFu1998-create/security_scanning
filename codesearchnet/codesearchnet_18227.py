def rm_back_refs(obj):
    """When removing an object with foreign fields, back-references from
    other objects to the current object should be deleted. This function
    identifies foreign fields of the specified object whose values are not
    None and which specify back-reference keys, then removes back-references
    from linked objects to the specified object.

    :param obj: Object for which back-references should be removed

    """
    for ref in _collect_refs(obj):
        ref['value']._remove_backref(
            ref['field_instance']._backref_field_name,
            obj,
            ref['field_name'],
            strict=False
        )