def record_match_subfields(rec, tag, ind1=" ", ind2=" ", sub_key=None,
                           sub_value='', sub_key2=None, sub_value2='',
                           case_sensitive=True):
    """
    Find subfield instances in a particular field.

    It tests values in 1 of 3 possible ways:
     - Does a subfield code exist? (ie does 773__a exist?)
     - Does a subfield have a particular value? (ie 773__a == 'PhysX')
     - Do a pair of subfields have particular values?
        (ie 035__2 == 'CDS' and 035__a == '123456')

    Parameters:
     * rec - dictionary: a bibrecord structure
     * tag - string: the tag of the field (ie '773')
     * ind1, ind2 - char: a single characters for the MARC indicators
     * sub_key - char: subfield key to find
     * sub_value - string: subfield value of that key
     * sub_key2 - char: key of subfield to compare against
     * sub_value2 - string: expected value of second subfield
     * case_sensitive - bool: be case sensitive when matching values

    :return: false if no match found, else provides the field position (int)
    """
    if sub_key is None:
        raise TypeError("None object passed for parameter sub_key.")

    if sub_key2 is not None and sub_value2 is '':
        raise TypeError("Parameter sub_key2 defined but sub_value2 is None, "
                        + "function requires a value for comparrison.")
    ind1, ind2 = _wash_indicators(ind1, ind2)

    if not case_sensitive:
        sub_value = sub_value.lower()
        sub_value2 = sub_value2.lower()

    for field in record_get_field_instances(rec, tag, ind1, ind2):
        subfields = dict(field_get_subfield_instances(field))
        if not case_sensitive:
            for k, v in subfields.iteritems():
                subfields[k] = v.lower()

        if sub_key in subfields:
            if sub_value is '':
                return field[4]
            else:
                if sub_value == subfields[sub_key]:
                    if sub_key2 is None:
                        return field[4]
                    else:
                        if sub_key2 in subfields:
                            if sub_value2 == subfields[sub_key2]:
                                return field[4]
    return False