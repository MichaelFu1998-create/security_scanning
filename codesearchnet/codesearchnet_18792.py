def record_get_field_values(rec, tag, ind1=" ", ind2=" ", code="",
                            filter_subfield_code="",
                            filter_subfield_value="",
                            filter_subfield_mode="e"):
    """Return the list of values for the specified field of the record.

    List can be filtered. Use filter_subfield_code
    and filter_subfield_value to search
    only in fields that have these values inside them as a subfield.
    filter_subfield_mode can have 3 different values:
    'e' for exact search
    's' for substring search
    'r' for regexp search

    Returns empty list if nothing was found.

    Parameters (tag, ind1, ind2, code) can contain wildcard %.

    :param rec: a record structure as returned by create_record()
    :param tag: a 3 characters long string
    :param ind1: a 1 character long string
    :param ind2: a 1 character long string
    :param code: a 1 character long string
    :return: a list of strings
    """
    tmp = []

    ind1, ind2 = _wash_indicators(ind1, ind2)

    if filter_subfield_code and filter_subfield_mode == "r":
        reg_exp = re.compile(filter_subfield_value)

    tags = []
    if '%' in tag:
        # Wild card in tag. Must find all corresponding tags and fields
        tags = [k for k in rec if _tag_matches_pattern(k, tag)]
    elif rec and tag in rec:
        tags = [tag]

    if code == '':
        # Code not specified. Consider field value (without subfields)
        for tag in tags:
            for field in rec[tag]:
                if (ind1 in ('%', field[1]) and ind2 in ('%', field[2]) and
                        field[3]):
                    tmp.append(field[3])
    elif code == '%':
        # Code is wildcard. Consider all subfields
        for tag in tags:
            for field in rec[tag]:
                if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                    if filter_subfield_code:
                        if filter_subfield_mode == "e":
                            subfield_to_match = (filter_subfield_code,
                                                 filter_subfield_value)
                            if subfield_to_match in field[0]:
                                for subfield in field[0]:
                                    tmp.append(subfield[1])
                        elif filter_subfield_mode == "s":
                            if (dict(field[0]).get(filter_subfield_code, '')) \
                                    .find(filter_subfield_value) > -1:
                                for subfield in field[0]:
                                    tmp.append(subfield[1])
                        elif filter_subfield_mode == "r":
                            if reg_exp.match(dict(field[0])
                                             .get(filter_subfield_code, '')):
                                for subfield in field[0]:
                                    tmp.append(subfield[1])
                    else:
                        for subfield in field[0]:
                            tmp.append(subfield[1])
    else:
        # Code is specified. Consider all corresponding subfields
        for tag in tags:
            for field in rec[tag]:
                if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                    if filter_subfield_code:
                        if filter_subfield_mode == "e":
                            subfield_to_match = (filter_subfield_code,
                                                 filter_subfield_value)
                            if subfield_to_match in field[0]:
                                for subfield in field[0]:
                                    if subfield[0] == code:
                                        tmp.append(subfield[1])
                        elif filter_subfield_mode == "s":
                            if (dict(field[0]).get(filter_subfield_code, '')) \
                                    .find(filter_subfield_value) > -1:
                                for subfield in field[0]:
                                    if subfield[0] == code:
                                        tmp.append(subfield[1])
                        elif filter_subfield_mode == "r":
                            if reg_exp.match(dict(field[0])
                                             .get(filter_subfield_code, '')):
                                for subfield in field[0]:
                                    if subfield[0] == code:
                                        tmp.append(subfield[1])
                    else:
                        for subfield in field[0]:
                            if subfield[0] == code:
                                tmp.append(subfield[1])

    # If tmp was not set, nothing was found
    return tmp