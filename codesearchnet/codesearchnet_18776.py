def record_get_field_instances(rec, tag="", ind1=" ", ind2=" "):
    """
    Return the list of field instances for the specified tag and indications.

    Return empty list if not found.
    If tag is empty string, returns all fields

    Parameters (tag, ind1, ind2) can contain wildcard %.

    :param rec: a record structure as returned by create_record()
    :param tag: a 3 characters long string
    :param ind1: a 1 character long string
    :param ind2: a 1 character long string
    :param code: a 1 character long string
    :return: a list of field tuples (Subfields, ind1, ind2, value,
             field_position_global) where subfields is list of (code, value)
    """
    if not rec:
        return []
    if not tag:
        return rec.items()
    else:
        out = []
        ind1, ind2 = _wash_indicators(ind1, ind2)

        if '%' in tag:
            # Wildcard in tag. Check all possible
            for field_tag in rec:
                if _tag_matches_pattern(field_tag, tag):
                    for possible_field_instance in rec[field_tag]:
                        if (ind1 in ('%', possible_field_instance[1]) and
                                ind2 in ('%', possible_field_instance[2])):
                            out.append(possible_field_instance)
        else:
            # Completely defined tag. Use dict
            for possible_field_instance in rec.get(tag, []):
                if (ind1 in ('%', possible_field_instance[1]) and
                        ind2 in ('%', possible_field_instance[2])):
                    out.append(possible_field_instance)
        return out