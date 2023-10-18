def download(server_path, local_path='.'):
    """
    Recursively download a file or item from the Midas Server instance.

    :param server_path: The location on the server to find the resource to
        download
    :type server_path: string
    :param local_path: The location on the client to store the downloaded data
    :type local_path: string
    """
    session.token = verify_credentials()

    is_item, resource_id = _find_resource_id_from_path(server_path)
    if resource_id == -1:
        print('Unable to locate {0}'.format(server_path))
    else:
        if is_item:
            _download_item(resource_id, local_path)
        else:
            _download_folder_recursive(resource_id, local_path)