def record_delete_subfield_from(rec, tag, subfield_position,
                                field_position_global=None,
                                field_position_local=None):
    """
    Delete subfield from position specified.

    Specify the subfield by tag, field number and subfield position.
    """
    subfields = record_get_subfields(
        rec, tag,
        field_position_global=field_position_global,
        field_position_local=field_position_local)

    try:
        del subfields[subfield_position]
    except IndexError:
        raise InvenioBibRecordFieldError(
            "The record does not contain the subfield "
            "'%(subfieldIndex)s' inside the field (local: "
            "'%(fieldIndexLocal)s, global: '%(fieldIndexGlobal)s' ) of tag "
            "'%(tag)s'." %
            {"subfieldIndex": subfield_position,
             "fieldIndexLocal": str(field_position_local),
             "fieldIndexGlobal": str(field_position_global),
             "tag": tag})
    if not subfields:
        if field_position_global is not None:
            for position, field in enumerate(rec[tag]):
                if field[4] == field_position_global:
                    del rec[tag][position]
        else:
            del rec[tag][field_position_local]

        if not rec[tag]:
            del rec[tag]