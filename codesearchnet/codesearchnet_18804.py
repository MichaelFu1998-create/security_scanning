def record_order_subfields(rec, tag=None):
    """
    Order subfields from a record alphabetically based on subfield code.

    If 'tag' is not None, only a specific tag of the record will be reordered,
    otherwise the whole record.

    :param rec: bibrecord
    :type rec: bibrec
    :param tag: tag where the subfields will be ordered
    :type tag: str
    """
    if rec is None:
        return rec
    if tag is None:
        tags = rec.keys()
        for tag in tags:
            record_order_subfields(rec, tag)
    elif tag in rec:
        for i in xrange(len(rec[tag])):
            field = rec[tag][i]
            # Order subfields alphabetically by subfield code
            ordered_subfields = sorted(field[0],
                                       key=lambda subfield: subfield[0])
            rec[tag][i] = (ordered_subfields, field[1], field[2], field[3],
                           field[4])