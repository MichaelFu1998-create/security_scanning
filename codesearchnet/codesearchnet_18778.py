def record_delete_field(rec, tag, ind1=' ', ind2=' ',
                        field_position_global=None, field_position_local=None):
    """
    Delete the field with the given position.

    If global field position is specified, deletes the field with the
    corresponding global field position.
    If field_position_local is specified, deletes the field with the
    corresponding local field position and tag.
    Else deletes all the fields matching tag and optionally ind1 and
    ind2.

    If both field_position_global and field_position_local are present,
    then field_position_local takes precedence.

    :param rec: the record data structure
    :param tag: the tag of the field to be deleted
    :param ind1: the first indicator of the field to be deleted
    :param ind2: the second indicator of the field to be deleted
    :param field_position_global: the global field position (record wise)
    :param field_position_local: the local field position (tag wise)
    :return: the list of deleted fields
    """
    error = _validate_record_field_positions_global(rec)
    if error:
        # FIXME one should write a message here.
        pass

    if tag not in rec:
        return False

    ind1, ind2 = _wash_indicators(ind1, ind2)

    deleted = []
    newfields = []

    if field_position_global is None and field_position_local is None:
        # Remove all fields with tag 'tag'.
        for field in rec[tag]:
            if field[1] != ind1 or field[2] != ind2:
                newfields.append(field)
            else:
                deleted.append(field)
        rec[tag] = newfields
    elif field_position_global is not None:
        # Remove the field with 'field_position_global'.
        for field in rec[tag]:
            if (field[1] != ind1 and field[2] != ind2 or
                    field[4] != field_position_global):
                newfields.append(field)
            else:
                deleted.append(field)
        rec[tag] = newfields
    elif field_position_local is not None:
        # Remove the field with 'field_position_local'.
        try:
            del rec[tag][field_position_local]
        except IndexError:
            return []

    if not rec[tag]:
        # Tag is now empty, remove it.
        del rec[tag]

    return deleted