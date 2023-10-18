def upload(file_pattern, destination='Private', leaf_folders_as_items=False,
           reuse_existing=False):
    """
    Upload a pattern of files. This will recursively walk down every tree in
    the file pattern to create a hierarchy on the server. As of right now, this
    places the file into the currently logged in user's home directory.

    :param file_pattern: a glob type pattern for files
    :type file_pattern: string
    :param destination: (optional) name of the midas destination folder,
        defaults to Private
    :type destination: string
    :param leaf_folders_as_items: (optional) whether leaf folders should have
        all files uploaded as single items
    :type leaf_folders_as_items: bool
    :param reuse_existing: (optional) whether to accept an existing item of the
        same name in the same location, or create a new one instead
    :type reuse_existing: bool
    """
    session.token = verify_credentials()

    # Logic for finding the proper folder to place the files in.
    parent_folder_id = None
    user_folders = session.communicator.list_user_folders(session.token)
    if destination.startswith('/'):
        parent_folder_id = _find_resource_id_from_path(destination)
    else:
        for cur_folder in user_folders:
            if cur_folder['name'] == destination:
                parent_folder_id = cur_folder['folder_id']
    if parent_folder_id is None:
        print('Unable to locate specified destination. Defaulting to {0}.'
              .format(user_folders[0]['name']))
        parent_folder_id = user_folders[0]['folder_id']

    for current_file in glob.iglob(file_pattern):
        current_file = os.path.normpath(current_file)
        if os.path.isfile(current_file):
            print('Uploading item from {0}'.format(current_file))
            _upload_as_item(os.path.basename(current_file),
                            parent_folder_id,
                            current_file,
                            reuse_existing)
        else:
            _upload_folder_recursive(current_file,
                                     parent_folder_id,
                                     leaf_folders_as_items,
                                     reuse_existing)