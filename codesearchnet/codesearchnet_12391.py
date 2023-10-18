def inv_entry_to_path(data):
    """
    Determine the path from the intersphinx inventory entry

    Discard the anchors between head and tail to make it
    compatible with situations where extra meta information is encoded.
    """
    path_tuple = data[2].split("#")
    if len(path_tuple) > 1:
        path_str = "#".join((path_tuple[0], path_tuple[-1]))
    else:
        path_str = data[2]
    return path_str