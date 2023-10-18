def record_modify_controlfield(rec, tag, controlfield_value,
                               field_position_global=None,
                               field_position_local=None):
    """Modify controlfield at position specified by tag and field number."""
    field = record_get_field(
        rec, tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    new_field = (field[0], field[1], field[2], controlfield_value, field[4])

    record_replace_field(
        rec, tag, new_field,
        field_position_global=field_position_global,
        field_position_local=field_position_local)