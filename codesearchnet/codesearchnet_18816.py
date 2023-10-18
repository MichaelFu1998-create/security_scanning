def _correct_record(record):
    """
    Check and correct the structure of the record.

    :param record: the record data structure
    :return: a list of errors found
    """
    errors = []

    for tag in record.keys():
        upper_bound = '999'
        n = len(tag)

        if n > 3:
            i = n - 3
            while i > 0:
                upper_bound = '%s%s' % ('0', upper_bound)
                i -= 1

        # Missing tag. Replace it with dummy tag '000'.
        if tag == '!':
            errors.append((1, '(field number(s): ' +
                              str([f[4] for f in record[tag]]) + ')'))
            record['000'] = record.pop(tag)
            tag = '000'
        elif not ('001' <= tag <= upper_bound or
                  tag in ('FMT', 'FFT', 'BDR', 'BDM')):
            errors.append(2)
            record['000'] = record.pop(tag)
            tag = '000'

        fields = []
        for field in record[tag]:
            # Datafield without any subfield.
            if field[0] == [] and field[3] == '':
                errors.append((8, '(field number: ' + str(field[4]) + ')'))

            subfields = []
            for subfield in field[0]:
                if subfield[0] == '!':
                    errors.append((3, '(field number: ' + str(field[4]) + ')'))
                    newsub = ('', subfield[1])
                else:
                    newsub = subfield
                subfields.append(newsub)

            if field[1] == '!':
                errors.append((4, '(field number: ' + str(field[4]) + ')'))
                ind1 = " "
            else:
                ind1 = field[1]

            if field[2] == '!':
                errors.append((5, '(field number: ' + str(field[4]) + ')'))
                ind2 = " "
            else:
                ind2 = field[2]

            fields.append((subfields, ind1, ind2, field[3], field[4]))

        record[tag] = fields

    return errors