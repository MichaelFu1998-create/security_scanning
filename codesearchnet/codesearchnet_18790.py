def record_move_subfield(rec, tag, subfield_position, new_subfield_position,
                         field_position_global=None,
                         field_position_local=None):
    """Move subfield at specified position.

    Sspecify the subfield by tag, field number and subfield position to new
    subfield position.
    """
    subfields = record_get_subfields(
        rec,
        tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    try:
        subfield = subfields.pop(subfield_position)
        subfields.insert(new_subfield_position, subfield)
    except IndexError:
        raise InvenioBibRecordFieldError(
            "There is no subfield with position '%d'." % subfield_position)