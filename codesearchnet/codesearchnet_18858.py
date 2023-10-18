def _create_or_reuse_folder(local_folder, parent_folder_id,
                            reuse_existing=False):
    """
    Create a folder from the local file in the midas folder corresponding to
    the parent folder id.

    :param local_folder: full path to a directory on the local file system
    :type local_folder: string
    :param parent_folder_id: id of parent folder on the Midas Server instance,
        where the folder will be added
    :type parent_folder_id: int | long
    :param reuse_existing: (optional) whether to accept an existing folder of
       the same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    local_folder_name = os.path.basename(local_folder)
    folder_id = None
    if reuse_existing:
        # check by name to see if the folder already exists in the folder
        children = session.communicator.folder_children(
            session.token, parent_folder_id)
        folders = children['folders']

        for folder in folders:
            if folder['name'] == local_folder_name:
                folder_id = folder['folder_id']
                break

    if folder_id is None:
        # create the item for the subdir
        new_folder = session.communicator.create_folder(session.token,
                                                        local_folder_name,
                                                        parent_folder_id)
        folder_id = new_folder['folder_id']

    return folder_id