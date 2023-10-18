def nfs_path_exists(path):
    """
        The normal HFS file system that your mac uses does not work the same way
        as the NFS file system.  In HFS, capitalization does not matter, but in
        NFS it does. This function checks if a folder exists in HFS file system
        using NFS semantics (case sensitive)
    """
    split_path = path.lstrip('/').split('/')
    recreated_path = '/'
    for path_element in split_path:
        if path_element not in os.listdir(recreated_path):
            return False
        recreated_path = "{}{}/".format(recreated_path, path_element)
    return True