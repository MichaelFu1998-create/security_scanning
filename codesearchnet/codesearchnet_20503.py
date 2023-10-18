def create_folder(dirpath, overwrite=False):
        """ Will create dirpath folder. If dirpath already exists and overwrite is False,
        will append a '+' suffix to dirpath until dirpath does not exist."""
        if not overwrite:
            while op.exists(dirpath):
                dirpath += '+'

        os.makedirs(dirpath, exist_ok=overwrite)
        return dirpath