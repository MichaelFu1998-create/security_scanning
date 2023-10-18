def record_delete_fields(rec, tag, field_positions_local=None):
    """
    Delete all/some fields defined with MARC tag 'tag' from record 'rec'.

    :param rec: a record structure.
    :type rec: tuple
    :param tag: three letter field.
    :type tag: string
    :param field_position_local: if set, it is the list of local positions
        within all the fields with the specified tag, that should be deleted.
        If not set all the fields with the specified tag will be deleted.
    :type field_position_local: sequence
    :return: the list of deleted fields.
    :rtype: list
    :note: the record is modified in place.
    """
    if tag not in rec:
        return []

    new_fields, deleted_fields = [], []

    for position, field in enumerate(rec.get(tag, [])):
        if field_positions_local is None or position in field_positions_local:
            deleted_fields.append(field)
        else:
            new_fields.append(field)

    if new_fields:
        rec[tag] = new_fields
    else:
        del rec[tag]

    return deleted_fields