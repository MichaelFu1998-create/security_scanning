def _check_field_validity(field):
    """
    Check if a field is well-formed.

    :param field: A field tuple as returned by create_field()
    :type field:  tuple
    :raise InvenioBibRecordFieldError: If the field is invalid.
    """
    if type(field) not in (list, tuple):
        raise InvenioBibRecordFieldError(
            "Field of type '%s' should be either "
            "a list or a tuple." % type(field))

    if len(field) != 5:
        raise InvenioBibRecordFieldError(
            "Field of length '%d' should have 5 "
            "elements." % len(field))

    if type(field[0]) not in (list, tuple):
        raise InvenioBibRecordFieldError(
            "Subfields of type '%s' should be "
            "either a list or a tuple." % type(field[0]))

    if type(field[1]) is not str:
        raise InvenioBibRecordFieldError(
            "Indicator 1 of type '%s' should be "
            "a string." % type(field[1]))

    if type(field[2]) is not str:
        raise InvenioBibRecordFieldError(
            "Indicator 2 of type '%s' should be "
            "a string." % type(field[2]))

    if type(field[3]) is not str:
        raise InvenioBibRecordFieldError(
            "Controlfield value of type '%s' "
            "should be a string." % type(field[3]))

    if type(field[4]) is not int:
        raise InvenioBibRecordFieldError(
            "Global position of type '%s' should "
            "be an int." % type(field[4]))

    for subfield in field[0]:
        if (type(subfield) not in (list, tuple) or
                len(subfield) != 2 or type(subfield[0]) is not str or
                type(subfield[1]) is not str):
            raise InvenioBibRecordFieldError(
                "Subfields are malformed. "
                "Should a list of tuples of 2 strings.")