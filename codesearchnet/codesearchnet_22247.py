def apply_types(use_types, guess_type, line):
    """Apply the types on the elements of the line"""
    new_line = {}
    for k, v in line.items():
        if use_types.has_key(k):
            new_line[k] = force_type(use_types[k], v)
        elif guess_type:
            new_line[k] = determine_type(v)
        else:
            new_line[k] = v
    return new_line