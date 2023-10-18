def write_csv(filename, header, data=None, rows=None, mode="w"):
    """Write the data to the specified filename
    
    Usage
    -----
    >>> write_csv(filename, header, data, mode=mode)

    Parameters
    ----------
    filename : str
        The name of the file

    header : list of strings
        The names of the columns (or fields):
        (fieldname1, fieldname2, ...)

    data : list of dictionaries (optional)
        [
         {fieldname1: a1, fieldname2: a2},
         {fieldname1: b1, fieldname2: b2},
         ...
        ]

    rows : list of lists (optional)
        [
        (a1, a2),
        (b1, b2),
        ...
        ]

    mode : str (optional)
        "w": write the data to the file by overwriting it
        "a": write the data to the file by appending them

    Returns
    -------
    None. A CSV file is written.

    """
    if data == rows == None:
        msg = "You must specify either data or rows"
        raise ValueError(msg)

    elif data != None and rows != None:
        msg = "You must specify either data or rows. Not both"
        raise ValueError(msg)

    data_header = dict((x, x) for x in header)

    with open(filename, mode) as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=header)
            if mode == "w":
                writer.writerow(data_header)
            writer.writerows(data)
        elif rows:
            writer = csv.writer(f)
            if mode == "w":
                writer.writerow(header)
            writer.writerows(rows)

    print "Saved %s." % filename