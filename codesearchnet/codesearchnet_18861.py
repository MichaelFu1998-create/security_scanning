def _upload_as_item(local_file, parent_folder_id, file_path,
                    reuse_existing=False):
    """
    Function for doing an upload of a file as an item. This should be a
    building block for user-level functions.

    :param local_file: name of local file to upload
    :type local_file: string
    :param parent_folder_id: id of parent folder on the Midas Server instance,
        where the item will be added
    :type parent_folder_id: int | long
    :param file_path: full path to the file
    :type file_path: string
    :param reuse_existing: (optional) whether to accept an existing item of the
        same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    current_item_id = _create_or_reuse_item(local_file, parent_folder_id,
                                            reuse_existing)
    _create_bitstream(file_path, local_file, current_item_id)
    for callback in session.item_upload_callbacks:
        callback(session.communicator, session.token, current_item_id)