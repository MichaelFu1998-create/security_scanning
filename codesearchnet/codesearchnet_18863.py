def _upload_folder_recursive(local_folder,
                             parent_folder_id,
                             leaf_folders_as_items=False,
                             reuse_existing=False):
    """
    Function to recursively upload a folder and all of its descendants.

    :param local_folder: full path to local folder to be uploaded
    :type local_folder: string
    :param parent_folder_id: id of parent folder on the Midas Server instance,
        where the new folder will be added
    :type parent_folder_id: int | long
    :param leaf_folders_as_items: (optional) whether leaf folders should have
        all files uploaded as single items
    :type leaf_folders_as_items: bool
    :param reuse_existing: (optional) whether to accept an existing item of the
        same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    if leaf_folders_as_items and _has_only_files(local_folder):
        print('Creating item from {0}'.format(local_folder))
        _upload_folder_as_item(local_folder, parent_folder_id, reuse_existing)
        return
    else:
        # do not need to check if folder exists, if it does, an attempt to
        # create it will just return the existing id
        print('Creating folder from {0}'.format(local_folder))
        new_folder_id = _create_or_reuse_folder(local_folder, parent_folder_id,
                                                reuse_existing)

        for entry in sorted(os.listdir(local_folder)):
            full_entry = os.path.join(local_folder, entry)
            if os.path.islink(full_entry):
                # os.walk skips symlinks by default
                continue
            elif os.path.isdir(full_entry):
                _upload_folder_recursive(full_entry,
                                         new_folder_id,
                                         leaf_folders_as_items,
                                         reuse_existing)
            else:
                print('Uploading item from {0}'.format(full_entry))
                _upload_as_item(entry,
                                new_folder_id,
                                full_entry,
                                reuse_existing)