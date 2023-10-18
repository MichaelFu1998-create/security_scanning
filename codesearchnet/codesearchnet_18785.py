def record_get_subfields(rec, tag, field_position_global=None,
                         field_position_local=None):
    """
    Return the subfield of the matching field.

    One has to enter either a global field position or a local field position.

    :return: a list of subfield tuples (subfield code, value).
    :rtype:  list
    """
    field = record_get_field(
        rec, tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    return field[0]