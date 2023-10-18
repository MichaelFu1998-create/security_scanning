def read_openke_translation(filename, delimiter='\t', entity_first=True):
    """Returns map with entity or relations from plain text."""
    result = {}
    with open(filename, "r") as f:
        _ = next(f) # pass the total entry number
        for line in f:
            line_slice = line.rstrip().split(delimiter)
            if not entity_first:
                line_slice = list(reversed(line_slice))
            result[line_slice[0]] = line_slice[1]

    return result