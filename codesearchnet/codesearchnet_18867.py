def _descend_folder_for_id(parsed_path, folder_id):
    """
    Descend a path to return a folder id starting from the given folder id.

    :param parsed_path: a list of folders from top to bottom of a hierarchy
    :type parsed_path: list[string]
    :param folder_id: The id of the folder from which to start the descent
    :type folder_id: int | long
    :returns: The id of the found folder or -1
    :rtype: int | long
    """
    if len(parsed_path) == 0:
        return folder_id

    session.token = verify_credentials()

    base_folder = session.communicator.folder_get(session.token,
                                                  folder_id)
    cur_folder_id = -1
    for path_part in parsed_path:
        cur_folder_id = base_folder['folder_id']
        cur_children = session.communicator.folder_children(
            session.token, cur_folder_id)
        for inner_folder in cur_children['folders']:
            if inner_folder['name'] == path_part:
                base_folder = session.communicator.folder_get(
                    session.token, inner_folder['folder_id'])
                cur_folder_id = base_folder['folder_id']
                break
        else:
            return -1
    return cur_folder_id