def _get_printable_columns(columns, row):
    """Return only the part of the row which should be printed.
    """
    if not columns:
        return row

    # Extract the column values, in the order specified.
    return tuple(row[c] for c in columns)