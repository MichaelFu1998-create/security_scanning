def _create_or_reuse_item(local_file, parent_folder_id, reuse_existing=False):
    """
    Create an item from the local file in the Midas Server folder corresponding
    to the parent folder id.

    :param local_file: full path to a file on the local file system
    :type local_file: string
    :param parent_folder_id: id of parent folder on the Midas Server instance,
        where the item will be added
    :type parent_folder_id: int | long
    :param reuse_existing: (optional) whether to accept an existing item of the
        same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    local_item_name = os.path.basename(local_file)
    item_id = None
    if reuse_existing:
        # check by name to see if the item already exists in the folder
        children = session.communicator.folder_children(
            session.token, parent_folder_id)
        items = children['items']

        for item in items:
            if item['name'] == local_item_name:
                item_id = item['item_id']
                break

    if item_id is None:
        # create the item for the subdir
        new_item = session.communicator.create_item(
            session.token, local_item_name, parent_folder_id)
        item_id = new_item['item_id']

    return item_id