def record_modify_subfield(rec, tag, subfield_code, value, subfield_position,
                           field_position_global=None,
                           field_position_local=None):
    """Modify subfield at specified position.

    Specify the subfield by tag, field number and subfield position.
    """
    subfields = record_get_subfields(
        rec, tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    try:
        subfields[subfield_position] = (subfield_code, value)
    except IndexError:
        raise InvenioBibRecordFieldError(
            "There is no subfield with position '%d'." % subfield_position)