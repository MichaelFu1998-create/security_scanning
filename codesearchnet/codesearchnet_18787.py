def record_add_subfield_into(rec, tag, subfield_code, value,
                             subfield_position=None,
                             field_position_global=None,
                             field_position_local=None):
    """Add subfield into specified position.

    Specify the subfield by tag, field number and optionally by subfield
    position.
    """
    subfields = record_get_subfields(
        rec, tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    if subfield_position is None:
        subfields.append((subfield_code, value))
    else:
        subfields.insert(subfield_position, (subfield_code, value))