def record_strip_empty_volatile_subfields(rec):
    """Remove unchanged volatile subfields from the record."""
    for tag in rec.keys():
        for field in rec[tag]:
            field[0][:] = [subfield for subfield in field[0]
                           if subfield[1][:9] != "VOLATILE:"]