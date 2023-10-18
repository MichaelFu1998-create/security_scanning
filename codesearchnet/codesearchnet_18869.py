def _find_resource_id_from_path(path):
    """
    Get a folder id from a path on the server.

    Warning: This is NOT efficient at all.

    The schema for this path is:
    path := "/users/<name>/" | "/communities/<name>" , {<subfolder>/}
    name := <firstname> , "_" , <lastname>

    :param path: The virtual path on the server.
    :type path: string
    :returns: a tuple indicating True or False about whether the resource is an
        item and id of the resource i.e. (True, item_id) or (False, folder_id)
    :rtype: (bool, int | long)
    """
    session.token = verify_credentials()

    parsed_path = path.split('/')
    if parsed_path[-1] == '':
        parsed_path.pop()
    if path.startswith('/users/'):
        parsed_path.pop(0)  # remove '' before /
        parsed_path.pop(0)  # remove 'users'
        name = parsed_path.pop(0)  # remove '<firstname>_<lastname>'
        firstname, lastname = name.split('_')
        end = parsed_path.pop()
        user = session.communicator.get_user_by_name(firstname, lastname)
        leaf_folder_id = _descend_folder_for_id(parsed_path, user['folder_id'])
        return _search_folder_for_item_or_folder(end, leaf_folder_id)
    elif path.startswith('/communities/'):
        print(parsed_path)
        parsed_path.pop(0)  # remove '' before /
        parsed_path.pop(0)  # remove 'communities'
        community_name = parsed_path.pop(0)  # remove '<community>'
        end = parsed_path.pop()
        community = session.communicator.get_community_by_name(community_name)
        leaf_folder_id = _descend_folder_for_id(parsed_path,
                                                community['folder_id'])
        return _search_folder_for_item_or_folder(end, leaf_folder_id)
    else:
        return False, -1