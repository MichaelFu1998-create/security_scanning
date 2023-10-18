def _record_sort_by_indicators(record):
    """Sort the fields inside the record by indicators."""
    for tag, fields in record.items():
        record[tag] = _fields_sort_by_indicators(fields)