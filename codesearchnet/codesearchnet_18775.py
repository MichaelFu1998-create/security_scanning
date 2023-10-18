def records_identical(rec1, rec2, skip_005=True, ignore_field_order=False,
                      ignore_subfield_order=False,
                      ignore_duplicate_subfields=False,
                      ignore_duplicate_controlfields=False):
    """
    Return True if rec1 is identical to rec2.

    It does so regardless of a difference in the 005 tag (i.e. the timestamp).
    """
    rec1_keys = set(rec1.keys())
    rec2_keys = set(rec2.keys())
    if skip_005:
        rec1_keys.discard("005")
        rec2_keys.discard("005")
    if rec1_keys != rec2_keys:
        return False
    for key in rec1_keys:
        if ignore_duplicate_controlfields and key.startswith('00'):
            if set(field[3] for field in rec1[key]) != \
                    set(field[3] for field in rec2[key]):
                return False
            continue

        rec1_fields = rec1[key]
        rec2_fields = rec2[key]
        if len(rec1_fields) != len(rec2_fields):
            # They already differs in length...
            return False
        if ignore_field_order:
            # We sort the fields, first by indicators and then by anything else
            rec1_fields = sorted(
                rec1_fields,
                key=lambda elem: (elem[1], elem[2], elem[3], elem[0]))
            rec2_fields = sorted(
                rec2_fields,
                key=lambda elem: (elem[1], elem[2], elem[3], elem[0]))
        else:
            # We sort the fields, first by indicators, then by global position
            # and then by anything else
            rec1_fields = sorted(
                rec1_fields,
                key=lambda elem: (elem[1], elem[2], elem[4], elem[3], elem[0]))
            rec2_fields = sorted(
                rec2_fields,
                key=lambda elem: (elem[1], elem[2], elem[4], elem[3], elem[0]))
        for field1, field2 in zip(rec1_fields, rec2_fields):
            if ignore_duplicate_subfields:
                if field1[1:4] != field2[1:4] or \
                        set(field1[0]) != set(field2[0]):
                    return False
            elif ignore_subfield_order:
                if field1[1:4] != field2[1:4] or \
                        sorted(field1[0]) != sorted(field2[0]):
                    return False
            elif field1[:4] != field2[:4]:
                return False
    return True