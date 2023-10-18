def _search_folder_for_item_or_folder(name, folder_id):
    """
    Find an item or folder matching the name. A folder will be found first if
    both are present.

    :param name: The name of the resource
    :type name: string
    :param folder_id: The folder to search within
    :type folder_id: int | long
    :returns: A tuple indicating whether the resource is an item an the id of
        said resource. i.e. (True, item_id) or (False, folder_id). Note that in
        the event that we do not find a result return (False, -1)
    :rtype: (bool, int | long)
    """
    session.token = verify_credentials()

    children = session.communicator.folder_children(session.token, folder_id)
    for folder in children['folders']:
        if folder['name'] == name:
            return False, folder['folder_id']  # Found a folder
    for item in children['items']:
        if item['name'] == name:
            return True, item['item_id']  # Found an item
    return False, -1