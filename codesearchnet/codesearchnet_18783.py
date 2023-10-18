def record_get_field(rec, tag, field_position_global=None,
                     field_position_local=None):
    """
    Return the the matching field.

    One has to enter either a global field position or a local field position.

    :return: a list of subfield tuples (subfield code, value).
    :rtype: list
    """
    if field_position_global is None and field_position_local is None:
        raise InvenioBibRecordFieldError(
            "A field position is required to "
            "complete this operation.")
    elif field_position_global is not None and \
            field_position_local is not None:
        raise InvenioBibRecordFieldError(
            "Only one field position is required "
            "to complete this operation.")
    elif field_position_global:
        if tag not in rec:
            raise InvenioBibRecordFieldError("No tag '%s' in record." % tag)

        for field in rec[tag]:
            if field[4] == field_position_global:
                return field
        raise InvenioBibRecordFieldError(
            "No field has the tag '%s' and the "
            "global field position '%d'." % (tag, field_position_global))
    else:
        try:
            return rec[tag][field_position_local]
        except KeyError:
            raise InvenioBibRecordFieldError("No tag '%s' in record." % tag)
        except IndexError:
            raise InvenioBibRecordFieldError(
                "No field has the tag '%s' and "
                "the local field position '%d'." % (tag, field_position_local))