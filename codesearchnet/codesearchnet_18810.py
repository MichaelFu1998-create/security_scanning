def _validate_record_field_positions_global(record):
    """
    Check if the global field positions in the record are valid.

    I.e., no duplicate global field positions and local field positions in the
    list of fields are ascending.

    :param record: the record data structure
    :return: the first error found as a string or None if no error was found
    """
    all_fields = []
    for tag, fields in record.items():
        previous_field_position_global = -1
        for field in fields:
            if field[4] < previous_field_position_global:
                return ("Non ascending global field positions in tag '%s'." %
                        tag)
            previous_field_position_global = field[4]
            if field[4] in all_fields:
                return ("Duplicate global field position '%d' in tag '%s'" %
                        (field[4], tag))