def _shift_field_positions_global(record, start, delta=1):
    """
    Shift all global field positions.

    Shift all global field positions with global field positions
    higher or equal to 'start' from the value 'delta'.
    """
    if not delta:
        return

    for tag, fields in record.items():
        newfields = []
        for field in fields:
            if field[4] < start:
                newfields.append(field)
            else:
                # Increment the global field position by delta.
                newfields.append(tuple(list(field[:4]) + [field[4] + delta]))
        record[tag] = newfields