def record_drop_duplicate_fields(record):
    """
    Return a record where all the duplicate fields have been removed.

    Fields are considered identical considering also the order of their
    subfields.
    """
    out = {}
    position = 0
    tags = sorted(record.keys())
    for tag in tags:
        fields = record[tag]
        out[tag] = []
        current_fields = set()
        for full_field in fields:
            field = (tuple(full_field[0]),) + full_field[1:4]
            if field not in current_fields:
                current_fields.add(field)
                position += 1
                out[tag].append(full_field[:4] + (position,))
    return out