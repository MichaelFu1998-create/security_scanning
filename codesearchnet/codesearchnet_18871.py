def _download_item(item_id, path='.', item=None):
    """
    Download the requested item to the specified path.

    :param item_id: The id of the item to be downloaded
    :type item_id: int | long
    :param path: (optional) the location to download the item
    :type path: string
    :param item: The dict of item info
    :type item: dict | None
    """
    session.token = verify_credentials()

    filename, content_iter = session.communicator.download_item(
        item_id, session.token)
    item_path = os.path.join(path, filename)
    print('Creating file at {0}'.format(item_path))
    out_file = open(item_path, 'wb')
    for block in content_iter:
        out_file.write(block)
    out_file.close()
    for callback in session.item_download_callbacks:
        if not item:
            item = session.communicator.item_get(session.token, item_id)
        callback(session.communicator, session.token, item, item_path)