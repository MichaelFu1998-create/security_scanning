def get_possible_paths(base_path, path_regex):
    """
    Looks for path_regex within base_path. Each match is append
    in the returned list.
    path_regex may contain subfolder structure.
    If any part of the folder structure is a

    :param base_path: str

    :param path_regex: str

    :return list of strings
    """
    if not path_regex:
        return []

    if len(path_regex) < 1:
        return []

    if path_regex[0] == os.sep:
        path_regex = path_regex[1:]

    rest_files = ''
    if os.sep in path_regex:
        #split by os.sep
        node_names = path_regex.partition(os.sep)
        first_node = node_names[0]
        rest_nodes = node_names[2]

        folder_names = filter_list(os.listdir(base_path), first_node)

        for nom in folder_names:
            new_base = op.join(base_path, nom)
            if op.isdir(new_base):
                rest_files = get_possible_paths(new_base, rest_nodes)
    else:
        rest_files = filter_list(os.listdir(base_path), path_regex)

    files = []
    if rest_files:
        files = [op.join(base_path, f) for f in rest_files]

    return files