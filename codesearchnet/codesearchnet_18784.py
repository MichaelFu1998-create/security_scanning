def record_replace_field(rec, tag, new_field, field_position_global=None,
                         field_position_local=None):
    """Replace a field with a new field."""
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

        replaced = False
        for position, field in enumerate(rec[tag]):
            if field[4] == field_position_global:
                rec[tag][position] = new_field
                replaced = True

        if not replaced:
            raise InvenioBibRecordFieldError(
                "No field has the tag '%s' and "
                "the global field position '%d'." %
                (tag, field_position_global))
    else:
        try:
            rec[tag][field_position_local] = new_field
        except KeyError:
            raise InvenioBibRecordFieldError("No tag '%s' in record." % tag)
        except IndexError:
            raise InvenioBibRecordFieldError(
                "No field has the tag '%s' and "
                "the local field position '%d'." % (tag, field_position_local))