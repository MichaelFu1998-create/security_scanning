def _create_folder(local_folder, parent_folder_id):
    """
    Function for creating a remote folder and returning the id. This should be
    a building block for user-level functions.

    :param local_folder: full path to a local folder
    :type local_folder: string
    :param parent_folder_id: id of parent folder on the Midas Server instance,
        where the new folder will be added
    :type parent_folder_id: int | long
    :returns: id of the remote folder that was created
    :rtype: int | long
    """
    new_folder = session.communicator.create_folder(
        session.token, os.path.basename(local_folder), parent_folder_id)
    return new_folder['folder_id']