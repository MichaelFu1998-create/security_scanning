def record_make_all_subfields_volatile(rec):
    """
    Turns all subfields to volatile
    """
    for tag in rec.keys():
        for field_position, field in enumerate(rec[tag]):
            for subfield_position, subfield in enumerate(field[0]):
                if subfield[1][:9] != "VOLATILE:":
                    record_modify_subfield(rec, tag, subfield[0], "VOLATILE:" + subfield[1],
                        subfield_position, field_position_local=field_position)