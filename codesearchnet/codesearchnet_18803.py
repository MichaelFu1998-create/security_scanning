def record_strip_controlfields(rec):
    """
    Remove all non-empty controlfields from the record.

    :param rec:  A record dictionary structure
    :type  rec:  dictionary
    """
    for tag in rec.keys():
        if tag[:2] == '00' and rec[tag][0][3]:
            del rec[tag]