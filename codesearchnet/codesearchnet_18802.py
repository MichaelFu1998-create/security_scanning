def record_strip_empty_fields(rec, tag=None):
    """
    Remove empty subfields and fields from the record.

    If 'tag' is not None, only a specific tag of the record will be stripped,
    otherwise the whole record.

    :param rec:  A record dictionary structure
    :type  rec:  dictionary
    :param tag:  The tag of the field to strip empty fields from
    :type  tag:  string
    """
    # Check whole record
    if tag is None:
        tags = rec.keys()
        for tag in tags:
            record_strip_empty_fields(rec, tag)

    # Check specific tag of the record
    elif tag in rec:
        # in case of a controlfield
        if tag[:2] == '00':
            if len(rec[tag]) == 0 or not rec[tag][0][3]:
                del rec[tag]

        #in case of a normal field
        else:
            fields = []
            for field in rec[tag]:
                subfields = []
                for subfield in field[0]:
                    # check if the subfield has been given a value
                    if subfield[1]:
                        # Always strip values
                        subfield = (subfield[0], subfield[1].strip())
                        subfields.append(subfield)
                if len(subfields) > 0:
                    new_field = create_field(subfields, field[1], field[2],
                                             field[3])
                    fields.append(new_field)
            if len(fields) > 0:
                rec[tag] = fields
            else:
                del rec[tag]