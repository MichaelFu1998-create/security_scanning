def remove_redundancies(levels):
    """
    There are repeats in the output from get_levels(). We
    want only the earliest occurrence (after it's reversed)
    """
    seen = []
    final = []
    for line in levels:
        new_line = []
        for item in line:
            if item not in seen:
                seen.append(item)
                new_line.append(item)
        final.append(new_line)
    return final