def record_move_fields(rec, tag, field_positions_local,
                       field_position_local=None):
    """
    Move some fields to the position specified by 'field_position_local'.

    :param rec: a record structure as returned by create_record()
    :param tag: the tag of the fields to be moved
    :param field_positions_local: the positions of the fields to move
    :param field_position_local: insert the field before that
                                 field_position_local. If unspecified, appends
                                 the fields :return: the field_position_local
                                 is the operation was successful
    """
    fields = record_delete_fields(
        rec, tag,
        field_positions_local=field_positions_local)
    return record_add_fields(
        rec, tag, fields,
        field_position_local=field_position_local)