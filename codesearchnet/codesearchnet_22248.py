def read_csv(filename, delimiter=",", skip=0, guess_type=True, has_header=True, use_types={}):
    """Read a CSV file
    
    Usage
    -----
    >>> data = read_csv(filename, delimiter=delimiter, skip=skip,
            guess_type=guess_type, has_header=True, use_types={}) 

    # Use specific types
    >>> types = {"sepal.length": int, "petal.width": float}
    >>> data = read_csv(filename, guess_type=guess_type, use_types=types) 

    keywords
    :has_header:
        Determine whether the file has a header or not

    """
    with open(filename, 'r') as f:
        # Skip the n first lines
        if has_header:
            header = f.readline().strip().split(delimiter)
        else:
            header = None

        for i in range(skip):
            f.readline()

        for line in csv.DictReader(f, delimiter=delimiter, fieldnames=header):
            if use_types:
                yield apply_types(use_types, guess_type, line)
            elif guess_type:
                yield dmap(determine_type, line)
            else:
                yield line