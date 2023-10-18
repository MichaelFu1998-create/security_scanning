def filter_field_instances(field_instances, filter_subcode, filter_value,
                           filter_mode='e'):
    """Filter the given field.

    Filters given field and returns only that field instances that contain
    filter_subcode with given filter_value. As an input for search function
    accepts output from record_get_field_instances function. Function can be
    run in three modes:

    - 'e' - looking for exact match in subfield value
    - 's' - looking for substring in subfield value
    - 'r' - looking for regular expression in subfield value

    Example:

    record_filter_field(record_get_field_instances(rec, '999', '%', '%'),
                        'y', '2001')

    In this case filter_subcode is 'y' and filter_value is '2001'.

    :param field_instances: output from record_get_field_instances
    :param filter_subcode: name of the subfield
    :type filter_subcode: string
    :param filter_value: value of the subfield
    :type filter_value: string
    :param filter_mode: 'e','s' or 'r'
    """
    matched = []
    if filter_mode == 'e':
        to_match = (filter_subcode, filter_value)
        for instance in field_instances:
            if to_match in instance[0]:
                matched.append(instance)
    elif filter_mode == 's':
        for instance in field_instances:
            for subfield in instance[0]:
                if subfield[0] == filter_subcode and \
                   subfield[1].find(filter_value) > -1:
                    matched.append(instance)
                    break
    elif filter_mode == 'r':
        reg_exp = re.compile(filter_value)
        for instance in field_instances:
            for subfield in instance[0]:
                if subfield[0] == filter_subcode and \
                   reg_exp.match(subfield[1]) is not None:
                    matched.append(instance)
                    break
    return matched