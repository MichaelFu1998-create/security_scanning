def _has_only_files(local_folder):
    """
    Return whether a folder contains only files. This will be False if the
    folder contains any subdirectories.

    :param local_folder: full path to the local folder
    :type local_folder: string
    :returns: True if the folder contains only files
    :rtype: bool
    """
    return not any(os.path.isdir(os.path.join(local_folder, entry))
                   for entry in os.listdir(local_folder))