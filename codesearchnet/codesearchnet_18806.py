def _compare_fields(field1, field2, strict=True):
    """
    Compare 2 fields.

    If strict is True, then the order of the subfield will be taken care of, if
    not then the order of the subfields doesn't matter.

    :return: True if the field are equivalent, False otherwise.
    """
    if strict:
        # Return a simple equal test on the field minus the position.
        return field1[:4] == field2[:4]
    else:
        if field1[1:4] != field2[1:4]:
            # Different indicators or controlfield value.
            return False
        else:
            # Compare subfields in a loose way.
            return set(field1[0]) == set(field2[0])