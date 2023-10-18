def to_csv(data, field_names=None, filename='data.csv',
           overwrite=True,
           write_headers=True, append=False, flat=True,
           primary_fields=None, sort_fields=True):
    """
    DEPRECATED    Write a list of dicts to a csv file

    :param data: List of dicts
    :param field_names: The list column names
    :param filename: The name of the file
    :param overwrite: Overwrite the file if exists
    :param write_headers: Write the headers to the csv file
    :param append: Write new rows if the file exists
    :param flat: Flatten the dictionary before saving
    :param primary_fields: The first columns of the csv file
    :param sort_fields: Sort the field names alphabetically
    :return: None
    """

    # Don't overwrite if not specified
    if not overwrite and path.isfile(filename):
        raise FileExistsError('The file already exists')

    # Replace file if append not specified
    write_type = 'w' if not append else 'a'

    # Flatten if flat is specified, or there are no predefined field names
    if flat or not field_names:
        data = [flatten(datum) for datum in data]

    # Fill in gaps between dicts with empty string
    if not field_names:
        field_names, data = fill_gaps(data)

    # Sort fields if specified
    if sort_fields:
        field_names.sort()

    # If there are primary fields, move the field names to the front and sort
    #  based on first field
    if primary_fields:
        for key in primary_fields[::-1]:
            field_names.insert(0, field_names.pop(field_names.index(key)))

        data = sorted(data, key=lambda k: k[field_names[0]], reverse=True)

    # Write the file
    with open(filename, write_type, encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names, lineterminator='\n')
        if not append or write_headers:
            writer.writeheader()

        # Write rows containing fields in field names
        for datum in data:
            for key in list(datum.keys()):
                if key not in field_names:
                    del datum[key]
                elif type(datum[key]) is str:
                    datum[key] = datum[key].strip()

                datum[key] = str(datum[key])

            writer.writerow(datum)