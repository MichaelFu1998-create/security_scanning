def record_get_field_value(rec, tag, ind1=" ", ind2=" ", code=""):
    """Return first (string) value that matches specified field of the record.

    Returns empty string if not found.

    Parameters (tag, ind1, ind2, code) can contain wildcard %.

    Difference between wildcard % and empty '':

    - Empty char specifies that we are not interested in a field which
      has one of the indicator(s)/subfield specified.

    - Wildcard specifies that we are interested in getting the value
      of the field whatever the indicator(s)/subfield is.

    For e.g. consider the following record in MARC::

        100C5  $$a val1
        555AB  $$a val2
        555AB      val3
        555    $$a val4
        555A       val5

    .. doctest::

        >>> record_get_field_value(record, '555', 'A', '', '')
        "val5"
        >>> record_get_field_value(record, '555', 'A', '%', '')
        "val3"
        >>> record_get_field_value(record, '555', 'A', '%', '%')
        "val2"
        >>> record_get_field_value(record, '555', 'A', 'B', '')
        "val3"
        >>> record_get_field_value(record, '555', '', 'B', 'a')
        ""
        >>> record_get_field_value(record, '555', '', '', 'a')
        "val4"
        >>> record_get_field_value(record, '555', '', '', '')
        ""
        >>> record_get_field_value(record, '%%%', '%', '%', '%')
        "val1"

    :param rec: a record structure as returned by create_record()
    :param tag: a 3 characters long string
    :param ind1: a 1 character long string
    :param ind2: a 1 character long string
    :param code: a 1 character long string
    :return: string value (empty if nothing found)
    """
    # Note: the code is quite redundant for speed reasons (avoid calling
    # functions or doing tests inside loops)
    ind1, ind2 = _wash_indicators(ind1, ind2)

    if '%' in tag:
        # Wild card in tag. Must find all corresponding fields
        if code == '':
            # Code not specified.
            for field_tag, fields in rec.items():
                if _tag_matches_pattern(field_tag, tag):
                    for field in fields:
                        if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                            # Return matching field value if not empty
                            if field[3]:
                                return field[3]
        elif code == '%':
            # Code is wildcard. Take first subfield of first matching field
            for field_tag, fields in rec.items():
                if _tag_matches_pattern(field_tag, tag):
                    for field in fields:
                        if (ind1 in ('%', field[1]) and
                                ind2 in ('%', field[2]) and field[0]):
                            return field[0][0][1]
        else:
            # Code is specified. Take corresponding one
            for field_tag, fields in rec.items():
                if _tag_matches_pattern(field_tag, tag):
                    for field in fields:
                        if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                            for subfield in field[0]:
                                if subfield[0] == code:
                                    return subfield[1]

    else:
        # Tag is completely specified. Use tag as dict key
        if tag in rec:
            if code == '':
                # Code not specified.
                for field in rec[tag]:
                    if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                        # Return matching field value if not empty
                        # or return "" empty if not exist.
                        if field[3]:
                            return field[3]

            elif code == '%':
                # Code is wildcard. Take first subfield of first matching field
                for field in rec[tag]:
                    if ind1 in ('%', field[1]) and ind2 in ('%', field[2]) and\
                            field[0]:
                        return field[0][0][1]
            else:
                # Code is specified. Take corresponding one
                for field in rec[tag]:
                    if ind1 in ('%', field[1]) and ind2 in ('%', field[2]):
                        for subfield in field[0]:
                            if subfield[0] == code:
                                return subfield[1]
    # Nothing was found
    return ""