def record_find_field(rec, tag, field, strict=False):
    """
    Return the global and local positions of the first occurrence of the field.

    :param rec:    A record dictionary structure
    :type  rec:    dictionary
    :param tag:    The tag of the field to search for
    :type  tag:    string
    :param field:  A field tuple as returned by create_field()
    :type  field:  tuple
    :param strict: A boolean describing the search method. If strict
                   is False, then the order of the subfields doesn't
                   matter. Default search method is strict.
    :type  strict: boolean
    :return:       A tuple of (global_position, local_position) or a
                   tuple (None, None) if the field is not present.
    :rtype:        tuple
    :raise InvenioBibRecordFieldError: If the provided field is invalid.
    """
    try:
        _check_field_validity(field)
    except InvenioBibRecordFieldError:
        raise

    for local_position, field1 in enumerate(rec.get(tag, [])):
        if _compare_fields(field, field1, strict):
            return (field1[4], local_position)

    return (None, None)