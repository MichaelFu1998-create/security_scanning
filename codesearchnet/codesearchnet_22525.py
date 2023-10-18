def copy_file(src, dest):
    """
    Copy file helper method

    :type src: str|unicode
    :type dest: str|unicode
    """
    dir_path = os.path.dirname(dest)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    shutil.copy2(src, dest)