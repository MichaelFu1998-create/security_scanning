def _upload_folder_as_item(local_folder, parent_folder_id,
                           reuse_existing=False):
    """
    Upload a folder as a new item. Take a folder and use its base name as the
    name of a new item. Then, upload its containing files into the new item as
    bitstreams.

    :param local_folder: The path to the folder to be uploaded
    :type local_folder: string
    :param parent_folder_id: The id of the destination folder for the new item.
    :type parent_folder_id: int | long
    :param reuse_existing: (optional) whether to accept an existing item of the
        same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    item_id = _create_or_reuse_item(local_folder, parent_folder_id,
                                    reuse_existing)

    subdir_contents = sorted(os.listdir(local_folder))
    # for each file in the subdir, add it to the item
    filecount = len(subdir_contents)
    for (ind, current_file) in enumerate(subdir_contents):
        file_path = os.path.join(local_folder, current_file)
        log_ind = '({0} of {1})'.format(ind + 1, filecount)
        _create_bitstream(file_path, current_file, item_id, log_ind)

    for callback in session.item_upload_callbacks:
        callback(session.communicator, session.token, item_id)