def record_add_fields(rec, tag, fields, field_position_local=None,
                      field_position_global=None):
    """
    Add the fields into the record at the required position.

    The position is specified by the tag and the field_position_local in the
    list of fields.

    :param rec: a record structure
    :param tag: the tag of the fields to be moved
    :param field_position_local: the field_position_local to which the field
                                 will be inserted. If not specified, appends
                                 the fields to the tag.
    :param a: list of fields to be added
    :return: -1 if the operation failed, or the field_position_local if it was
             successful
    """
    if field_position_local is None and field_position_global is None:
        for field in fields:
            record_add_field(
                rec, tag, ind1=field[1],
                ind2=field[2], subfields=field[0],
                controlfield_value=field[3])
    else:
        fields.reverse()
        for field in fields:
            record_add_field(
                rec, tag, ind1=field[1], ind2=field[2],
                subfields=field[0], controlfield_value=field[3],
                field_position_local=field_position_local,
                field_position_global=field_position_global)

    return field_position_local