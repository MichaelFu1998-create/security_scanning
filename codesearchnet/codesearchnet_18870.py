def _download_folder_recursive(folder_id, path='.'):
    """
    Download a folder to the specified path along with any children.

    :param folder_id: The id of the target folder
    :type folder_id: int | long
    :param path: (optional) the location to download the folder
    :type path: string
    """
    session.token = verify_credentials()

    cur_folder = session.communicator.folder_get(session.token, folder_id)
    # Replace any '/' in the folder name.
    folder_path = os.path.join(path, cur_folder['name'].replace('/', '_'))
    print('Creating folder at {0}'.format(folder_path))
    try:
        os.mkdir(folder_path)
    except OSError as e:
        if e.errno == errno.EEXIST and session.allow_existing_download_paths:
            pass
        else:
            raise
    cur_children = session.communicator.folder_children(
        session.token, folder_id)
    for item in cur_children['items']:
        _download_item(item['item_id'], folder_path, item=item)
    for folder in cur_children['folders']:
        _download_folder_recursive(folder['folder_id'], folder_path)
    for callback in session.folder_download_callbacks:
        callback(session.communicator, session.token, cur_folder, folder_path)