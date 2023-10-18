def rm_fwd_refs(obj):
    """When removing an object, other objects with references to the current
    object should remove those references. This function identifies objects
    with forward references to the current object, then removes those
    references.

    :param obj: Object to which forward references should be removed

    """
    for stack, key in obj._backrefs_flat:

        # Unpack stack
        backref_key, parent_schema_name, parent_field_name = stack

        # Get parent info
        parent_schema = obj._collections[parent_schema_name]
        parent_key_store = parent_schema._pk_to_storage(key)
        parent_object = parent_schema.load(parent_key_store)
        if parent_object is None:
            continue

        # Remove forward references
        if parent_object._fields[parent_field_name]._list:
            getattr(parent_object, parent_field_name).remove(obj)
        else:
            parent_field_object = parent_object._fields[parent_field_name]
            setattr(parent_object, parent_field_name, parent_field_object._gen_default())

        # Save
        parent_object.save()