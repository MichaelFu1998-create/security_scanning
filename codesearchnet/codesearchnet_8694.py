def parse_csv(file_stream, expected_columns=None):
    """
    Parse csv file and return a stream of dictionaries representing each row.

    First line of CSV file must contain column headers.

    Arguments:
         file_stream: input file
         expected_columns (set[unicode]): columns that are expected to be present

    Yields:
        dict: CSV line parsed into a dictionary.
    """
    reader = unicodecsv.DictReader(file_stream, encoding="utf-8")

    if expected_columns and set(expected_columns) - set(reader.fieldnames):
        raise ValidationError(ValidationMessages.MISSING_EXPECTED_COLUMNS.format(
            expected_columns=", ".join(expected_columns), actual_columns=", ".join(reader.fieldnames)
        ))

    # "yield from reader" would be nicer, but we're on python2.7 yet.
    for row in reader:
        yield row